import os
from openai import OpenAI
import json

#OpenAI API Key Management
def get_api_key_from_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config.get("openai_api_key")

# Initialize OpenAI client
def get_openai_client():
    """Returns an OpenAI client using the provided API key."""
    API_KEY = get_api_key_from_config()
    if not API_KEY:
        raise ValueError("OpenAI API key not found. Please set it in config.json.")
    return OpenAI(api_key=API_KEY)

# Function to generate test case prompt
def create_prompt(context, num_cases=5):
    """Generates a structured prompt for test case generation."""
    return f"""
    You are an expert in financial transactions and risk assessment. Generate {num_cases} test cases for the following scenario:
    
    Scenario: {context}
    
    Each test case should include:
    - Test Case ID
    - Description
    - Expected Outcome
    - Risk Level (Low, Medium, High)
    - Regulatory Compliance Notes (if applicable)
    
    Format the output as a structured JSON list.
    """

# Function to interact with GPT model
def generate_test_cases(context, num_cases=5):
    """Calls GPT to generate test cases for a given financial scenario."""
    client = get_openai_client()
    prompt = create_prompt(context, num_cases)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI test case generator."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

# Main Execution

if __name__ == "__main__":
    context = "Detect fraudulent credit card transactions based on unusual spending patterns."
    test_cases = generate_test_cases(context)
    print(json.dumps(test_cases, indent=4))

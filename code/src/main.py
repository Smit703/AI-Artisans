import requests
import json

# Load API key from config file
def load_config():
    """Loads configuration settings from config.json."""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

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

def generate_test_cases(context, num_cases=5):
    """Calls Hugging Face model to generate test cases for a financial scenario."""
    prompt = create_prompt(context, num_cases)
    payload = {"inputs": prompt}

    CONFIG = load_config()
    API_URL = CONFIG["api_url"]
    HEADERS = {"Authorization": f"Bearer {CONFIG['api_key']}"}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        generated_text = response.json()[0].get("generated_text", "")
        return generated_text
    else:
        print("Error:", response.text)
        return None
    

# Main Execution
if __name__ == "__main__":
    context = "Detect fraudulent credit card transactions based on unusual spending patterns."
    test_cases = generate_test_cases(context)
    print(test_cases)
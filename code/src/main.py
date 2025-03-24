from flask import Flask, request, render_template, jsonify
import json
import google.generativeai as genai

app = Flask(__name__)

# Load API key from config file
def load_config():
    """Loads configuration settings from config.json."""
    with open("config.json", "r") as config_file:
        return json.load(config_file)
    
def load_instructions():
    """Loads additional instructions from instructions.md."""
    with open("instructions.md", "r") as instructions_file:
        return instructions_file.read()

def generate_tests_prompt(context, num_cases=10):
    """Generates a structured prompt for test case generation."""
    instructions = load_instructions()
    return f"""
    You are an expert in financial transactions and risk assessment. Generate {num_cases} test cases for the following scenario:
    
    Scenario: {context}

    Based on the context, follow these instructions:
    {instructions}
    
    Each test case should include:
    - Test Case ID
    - Description
    - Input data
    - Expected output
    - Validation steps
    - Expected Outcome

    Validate the test cases for accuracy, completeness, and relevance.

    Analyze and add:
    - Missing test scenarios and edge cases
    
    Format the output as a structured JSON list.
    """

def generate_test_cases(context, num_cases=5):
    """Calls Gemini API to generate test cases for a financial scenario."""
    prompt = generate_tests_prompt(context, num_cases)

    CONFIG = load_config()
    API_KEY = CONFIG["gemini_api_key"]

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        response = model.generate_content(prompt)
        test_cases = response.text 
        print(test_cases)
        return test_cases
    except Exception as e:
        print("Error:", str(e))
        return str(e)
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        context = request.form.get("context")
        num_cases = int(request.form.get("num_cases", 10))
        test_cases = generate_test_cases(context, num_cases)
        return jsonify(test_cases)
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=False)

# Main Execution
# if __name__ == "__main__":
#     context = "Detect fraudulent credit card transactions based on unusual spending patterns."
#     test_cases = generate_test_cases(context)
#     print(test_cases)
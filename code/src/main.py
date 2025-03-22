from flask import Flask, request, render_template, jsonify
import requests
import json

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

    Based on the context follow the instructions {instructions} to generate the test cases.
    
    Each test case should include:
    - Test Case ID
    - Description
    - Input data
    - Expected output
    - Validation steps
    - Expected Outcome

    Validate the test cases for accuracy, completeness and relevance.

    Analyse and add:
    - Missing test scenarios and edge cases
    
    Format the output as a structured JSON list.
    """

def generate_test_cases(context, num_cases=5):
    """Calls Hugging Face model to generate test cases for a financial scenario."""
    prompt = generate_tests_prompt(context, num_cases)
    payload = {"inputs": prompt}

    CONFIG = load_config()
    API_URL = CONFIG["api_url"]
    HEADERS = {"Authorization": f"Bearer {CONFIG['api_key']}"}
    generated_tests = requests.post(API_URL, headers=HEADERS, json=payload)

    if generated_tests.status_code == 200:
        tests = generated_tests.json()[0].get("generated_text", "")
        print(tests)
        return tests
    else:
        error = generated_tests.text
        print("Error:", error)
        return error
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        context = request.form.get("context")
        num_cases = int(request.form.get("num_cases", 5))
        test_cases = generate_test_cases(context, num_cases)
        return jsonify(test_cases)
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=False)

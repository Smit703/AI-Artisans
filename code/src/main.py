from flask import Flask, request, render_template, send_file, jsonify
import json
import google.generativeai as genai
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
Test_case_file = os.path.join(script_dir, "Generated/test_cases.txt")

app = Flask(__name__)

def load_config():
    file_path = os.path.join(script_dir, "config.json")
    with open(file_path, "r") as config_file:
        return json.load(config_file)

def load_instructions():
    file_path = os.path.join(script_dir, "instructions.md")
    with open(file_path, "r") as instructions_file:
        return instructions_file.read()

def generate_tests_prompt(context, num_cases=10):
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
    
    Format the output as a structured JSON file.
    """

def generate_test_cases(context, num_cases=5):
    prompt = generate_tests_prompt(context, num_cases)
    CONFIG = load_config()
    API_KEY = CONFIG["gemini_api_key"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    try:
        response = model.generate_content(prompt)
        test_cases = response.text.strip()
        save_to_txt(test_cases)
        return jsonify({"message": "Test cases generated successfully."})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})

def save_to_txt(test_cases):
    with open(Test_case_file, "w") as file:
        file.write(test_cases)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        context = request.form.get("context")
        num_cases = int(request.form.get("num_cases", 10))
        return generate_test_cases(context, num_cases)
    return render_template("index.html")

@app.route("/download")
def download_file():
    return send_file(Test_case_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)
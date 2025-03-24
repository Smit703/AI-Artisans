from flask import Flask, request, render_template, send_file, jsonify
from openpyxl import load_workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
import json
import google.generativeai as genai
import os
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_file_path = os.path.join(script_dir, "Generated/test_cases.xlsx")
hasCode = False

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
    - Test scenario (gherkin format)
    - Test data (use '<br>' for line breaks)
    - Validation steps (use '<br>' for line breaks)
    - Expected Results (use '<br>' for line breaks)
    
    Validate the test cases for accuracy, completeness, and relevance.
    
    Analyze and add:
    - Missing test scenarios and edge cases
    
    Format the output as a table with the following columns:
    | Test Case ID | Test Scenario | Test Data | Validation Steps | Expected Results
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
        save_to_excel(test_cases, context)
        return jsonify({"message": "Test cases generated successfully."})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})

def save_to_excel(test_cases, context):
    rows = []
    lines = test_cases.split("\n")
    headers = ["Test Case ID", "BDD Format test case", "Test Data", "Validation Steps", "Expected Results"]
    
    for line in lines[4:]:
        if line.strip(): 
            columns = [cell.strip() for cell in line.split("|")[1:-1]] 
           
            columns[1] = columns[1].replace("Given", "**Given**").replace("When", "**When**").replace("Then", "**Then**")
           
            for i in range(2, 5): 
                if "<br>" in columns[i]: 
                    lines_in_column = columns[i].split("<br>")
                    numbered_lines = [
                        f"{idx + 1}. {line.strip()}" if not line.strip().startswith(f"{idx + 1}.") else line.strip()
                        for idx, line in enumerate(lines_in_column) if line.strip()
                    ]
                    columns[i] = "\n".join(numbered_lines)

            rows.append(columns)

    df = pd.DataFrame(rows, columns=headers)
    df.to_excel(excel_file_path, index=False, engine='openpyxl')
    
    workbook = load_workbook(excel_file_path)
    sheet = workbook.active

    header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    for cell in sheet[1]:  
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    table_range = f"A1:E{len(rows) + 2}" 
    table = Table(displayName="TestCasesTable", ref=table_range)

    style = TableStyleInfo(
        name="TableStyleMedium9", 
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=False,
        showColumnStripes=False,
    )
    table.tableStyleInfo = style
    sheet.add_table(table)

    for row in sheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)

    workbook.save(excel_file_path)
    print(f"Test cases saved to {excel_file_path}")        

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        context = request.form.get("context")
        num_cases = int(request.form.get("num_cases", 10))

        file_content = ""
        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename != "":
                file_content = uploaded_file.read().decode("utf-8")
                hasCode = True
            else:
                hasCode = False

        return generate_test_cases(context, num_cases)
    return render_template("index.html")

@app.route("/download")
def download_file():
    return send_file(excel_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)
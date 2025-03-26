import pytest
from LoanApproval import LoanApproval

def test_TC_Loan_001():
    loan = LoanApproval(income=70000, credit_score=720, debt=500, employment_status="Full-time", loan_amount=20000, loan_term=5)
    assert loan.is_eligible() == "Approved"

def test_TC_Loan_002():
    loan = LoanApproval(income=50000, credit_score=580, debt=500, employment_status="Full-time", loan_amount=20000, loan_term=5)
    assert loan.is_eligible() == "Rejected: Low Credit Score"

def test_TC_Loan_003():
    loan = LoanApproval(income=30000, credit_score=700, debt=1500, employment_status="Full-time", loan_amount=20000, loan_term=5)
    assert loan.is_eligible() == "Rejected: High Debt-to-Income Ratio"

def test_TC_Loan_004():
    loan = LoanApproval(income=15000, credit_score=700, debt=500, employment_status="Full-time", loan_amount=20000, loan_term=5)
    assert loan.is_eligible() == "Rejected: Low Income"

def test_TC_Loan_005():
    loan = LoanApproval(income=50000, credit_score=700, debt=500, employment_status="Unemployed", loan_amount=20000, loan_term=5)
    assert loan.is_eligible() == "Rejected: Unstable Employment"

def test_TC_Loan_006():
    loan = LoanApproval(income=40000, credit_score=700, debt=500, employment_status="Full-time", loan_amount=30000, loan_term=5)
    assert loan.is_eligible() == "Rejected: Loan Payment Exceeds Affordable Amount"

def test_TC_Loan_007():
    loan = LoanApproval(income=0, credit_score=700, debt=0, employment_status="Full-time", loan_amount=20000, loan_term=5)
    assert loan.is_eligible() == "Rejected: Low Income"

def test_TC_Loan_008():
    loan = LoanApproval(income=25000, credit_score=750, debt=2000, employment_status="Full-time", loan_amount=10000, loan_term=3)
    assert loan.is_eligible() == "Rejected: High Debt-to-Income Ratio"

def test_TC_Loan_009():
    loan = LoanApproval(income=60000, credit_score=600, debt=500, employment_status="Full-time", loan_amount=15000, loan_term=4)
    assert loan.is_eligible() == "Approved"

def test_TC_Loan_010():
    loan = LoanApproval(income=40000, credit_score=650, debt=300, employment_status="Part-time", loan_amount=10000, loan_term=2)
    assert loan.is_eligible() == "Approved"
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Business Logic: Function to calculate credit score based on the input
def calculate_credit_score(income, default_record, employment_status):
    # Simplified scoring logic
    score = 500  # Base score

    # Adjust score based on income
    if income > 3000:
        score += 50
    elif income > 1000:
        score += 20

    # Adjust score based on default record
    if default_record.lower() == "no":
        score += 100
    else:
        score -= 100

    # Adjust score based on employment status
    if employment_status == "Employed":
        score += 50
    elif employment_status == "Self-employed":
        score += 30

    return score

# Logic for loan approval based on credit score
def approve_loan(credit_score, loan_amount):
    if credit_score > 600:
        if loan_amount <= 50000:
            return "Approved"
        else:
            return "Rejected: Loan amount exceeds limit"
    else:
        return "Rejected: Insufficient credit score"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    bank_account = request.form['bank_account']
    employment_status = request.form['employment_status']
    income = float(request.form['income'])
    default_record = request.form['default_record']
    loan_amount = float(request.form['loan_amount'])
    loan_period = int(request.form['loan_period'])
    loan_usage = request.form['loan_usage']

    # Calculate credit score
    credit_score = calculate_credit_score(income, default_record, employment_status)

    # Loan approval logic
    approval_status = approve_loan(credit_score, loan_amount)

    return f"Application for {name}: Credit Score: {credit_score}, Status: {approval_status}"

if __name__ == "__main__":
    app.run(debug=True)

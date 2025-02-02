from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Dummy function for calculating credit score
def calculate_credit_score(income, employment_status, default_record):
    score = 0
    if income >= 5000:
        score += 30
    if employment_status == "Employed":
        score += 20
    if default_record == "No":
        score += 50
    return score

# Dummy function for loan approval based on credit score
def loan_approval(credit_score, loan_amount):
    if credit_score >= 70:
        if loan_amount <= 100000:
            return "Approved"
        else:
            return "Denied"
    else:
        return "Denied"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    name = data.get('name')
    account = data.get('account')
    employment_status = data.get('employment')
    income = float(data.get('income'))
    default_record = data.get('default')
    loan_amount = float(data.get('loanAmount'))
    loan_period = int(data.get('loanPeriod'))
    loan_usage = data.get('loanUsage')

    credit_score = calculate_credit_score(income, employment_status, default_record)
    approval_status = loan_approval(credit_score, loan_amount)

    return jsonify({'credit_score': credit_score, 'loan_approval': approval_status})

if __name__ == '__main__':
    app.run(debug=True)

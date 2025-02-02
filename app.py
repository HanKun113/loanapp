from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# 计算信用分
def calculate_credit_score(income, default_record, employment_status):
    score = 500  # 初始分数

    # 收入影响
    if income > 3000:
        score += 50
    elif income > 1000:
        score += 20

    # 默认记录影响
    if default_record.lower() == "no":
        score += 100
    else:
        score -= 100

    # 就业状态影响
    if employment_status == "Employed":
        score += 50
    elif employment_status == "Self-employed":
        score += 30

    return score

# 贷款审批逻辑
def approve_loan(credit_score, loan_amount):
    loan_limits = {
        600: 50000,
        700: 100000,
        800: 200000
    }
    
    for score, max_loan in loan_limits.items():
        if credit_score >= score and loan_amount <= max_loan:
            return "Approved", max_loan
    return "Rejected", None

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

    # 计算信用分
    credit_score = calculate_credit_score(income, default_record, employment_status)

    # 贷款审批
    approval_status, max_loan = approve_loan(credit_score, loan_amount)

    # 如果审批未通过，显示信用分和最低要求
    if approval_status == "Rejected":
        required_score = next((score for score, max_loan in sorted(loan_limits.items(), reverse=True) if loan_amount <= max_loan), None)
        return render_template('approval_result.html', approval_status=approval_status, credit_score=credit_score, required_score=required_score, loan_amount=loan_amount)

    # 如果审批通过，显示贷款额度和时长
    return render_template('approval_result.html', approval_status=approval_status, credit_score=credit_score, loan_amount=loan_amount, loan_period=loan_period)

if __name__ == "__main__":
    app.run(debug=True)

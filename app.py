from flask import Flask, request, jsonify, render_template, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate_loan', methods=['POST'])
def evaluate_loan():
    data = request.form 
    
    credit_score = calculate_credit_score(data)
    
    decision = "Approved" if credit_score >= 70 else "Denied"
    
    loan_amount = float(data['loanAmount'])
    loan_period = int(data['loanPeriod'])
    
    risk_analysis = get_risk_analysis(credit_score, data)
    
    required_score = 70
    if credit_score < required_score:
        return redirect(url_for('loan_result', decision=decision, credit_score=credit_score, loan_amount=loan_amount, loan_period=loan_period, required_score=required_score))
    
    return redirect(url_for('loan_result', decision=decision, credit_score=credit_score, loan_amount=loan_amount, loan_period=loan_period))

@app.route('/loan_result')
def loan_result():
    decision = request.args.get('decision')
    credit_score = int(request.args.get('credit_score'))
    loan_amount = float(request.args.get('loan_amount'))
    loan_period = int(request.args.get('loan_period'))
    required_score = int(request.args.get('required_score', 0))  # 默认值为 0
    
    return render_template('loan_result.html', decision=decision, credit_score=credit_score, loan_amount=loan_amount, loan_period=loan_period, required_score=required_score)

def calculate_credit_score(data):
    score = 0
    
    employment_scores = {
        'employed': 20,
        'self-employed': 15,
        'retired': 10,
        'unemployed': 0
    }
    score += employment_scores.get(data['employmentStatus'], 0)
    
    monthly_income = float(data['income'])
    loan_amount = float(data['loanAmount'])
    
    income_ratio = (monthly_income * float(data['loanPeriod'])) / loan_amount
    if income_ratio > 2.0:
        score += 30
    elif income_ratio > 1.5:
        score += 20
    elif income_ratio > 1.0:
        score += 10
    
    if data['defaultRecord'] == 'no':
        score += 30
    
    purpose_scores = {
        'business': 20,
        'house': 18,
        'education': 15,
        'car': 12,
        'personal': 10,
        'other': 5
    }
    score += purpose_scores.get(data['loanUsage'], 5)
    
    return score

def get_risk_analysis(score, data):
    analysis = []
    
    if score >= 80:
        analysis.append("Low risk applicant")
    elif score >= 60:
        analysis.append("Medium risk applicant")
    else:
        analysis.append("High risk applicant")
    
    monthly_income = float(data['income'])
    loan_amount = float(data['loanAmount'])
    
    if loan_amount > monthly_income * 24:
        analysis.append("Loan amount is significantly high compared to income")
    if data['defaultRecord'] == 'yes':
        analysis.append("Previous default history is a concern")
    if float(data['loanPeriod']) > 180:
        analysis.append("Long loan period increases risk")
    
    return "; ".join(analysis)

if __name__ == '__main__':
    app.run(debug=True)

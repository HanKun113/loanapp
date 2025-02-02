from flask import Flask,request,jsonify, render_template
import textblob
import os
import google.generativeai as genai

# 显示表单的路由
@app.route('/')
def index():
    return render_template('index.html')

# 处理贷款评估的路由
@app.route('/evaluate_loan', methods=['POST'])
def evaluate_loan():
    data = request.json
    
    # 计算信用分数
    credit_score = calculate_credit_score(data)
    
    # 确定贷款决定
    decision = "Approved" if credit_score >= 70 else "Denied"
    
    # 获取风险分析
    risk_analysis = get_risk_analysis(credit_score, data)
    
    return jsonify({
        'credit_score': credit_score,
        'decision': decision,
        'risk_analysis': risk_analysis
    })

# 计算信用分数的函数
def calculate_credit_score(data):
    score = 0
    
    # 就业状态评分 (0-20分)
    employment_scores = {
        'employed': 20,
        'self-employed': 15,
        'retired': 10,
        'unemployed': 0
    }
    score += employment_scores.get(data['employmentStatus'], 0)
    
    # 收入评分 (0-30分)
    monthly_income = float(data['income'])
    loan_amount = float(data['loanAmount'])
    
    # 收入与贷款比率
    income_ratio = (monthly_income * float(data['loanPeriod'])) / loan_amount
    if income_ratio > 2.0:
        score += 30
    elif income_ratio > 1.5:
        score += 20
    elif income_ratio > 1.0:
        score += 10
    
    # 违约记录评分 (0-30分)
    if data['defaultRecord'] == 'no':
        score += 30
    
    # 贷款用途评分 (0-20分)
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

# 生成风险分析的函数
def get_risk_analysis(score, data):
    analysis = []
    
    if score >= 80:
        analysis.append("Low risk applicant")
    elif score >= 60:
        analysis.append("Medium risk applicant")
    else:
        analysis.append("High risk applicant")
    
    # 添加具体风险因素
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
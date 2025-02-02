from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # 获取表单数据
    form_data = request.form
    # 将表单数据作为URL参数传递给结果页面
    params = '&'.join(f'{key}={value}' for key, value in form_data.items())
    return redirect(f'/result?{params}')

@app.route('/result', methods=['GET'])
def show_result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
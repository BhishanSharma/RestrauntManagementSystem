from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/bill')
def bill():
    return render_template('bill.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

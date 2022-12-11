from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'mudar depois'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    return render_template('inscricao.html')

if __name__ == '__main__':
    app.run(debug=True)

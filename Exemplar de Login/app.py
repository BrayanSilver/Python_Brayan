from flask import Flask, request, render_template_string, redirect, url_for
import hashlib

app = Flask(__name__)


users = {
    "user@example.com": hashlib.sha256("password123".encode()).hexdigest()  # Senha hashada
}

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/login', methods=['POST'])
def login():
    email = request.form['admin@admin']
    password = request.form['admin123']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if users.get(email) == hashed_password:
        return "Login bem-sucedido!"
    else:
        return "Email ou senha incorretos.", 403

@app.route('/forgot-password')
def forgot_password():
    return "Página de recuperação de senha"

@app.route('/signup')
def signup():
    return "Página de cadastro"

if __name__ == '__main__':
    app.run(debug=True)

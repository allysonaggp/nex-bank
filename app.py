from flask import Flask, request, render_template
from dbapi import consultar_conta_site, inserir_registro

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")  # pagina de login


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")  # pagina de login


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    if consultar_conta_site(usuario, senha) == True:
        return render_template("home.html")
    else:
        return "Usuario ou senha incorretos"


@app.route("/cadastro", methods=["POST"])
def registrar():
    usuario = request.form["usuario"]
    email = request.form["email"]
    cpf = request.form["cpf"]
    senha = request.form["senha"]
    inserir_registro(usuario, email, cpf, senha)
    if consultar_conta_site(usuario, senha) == True:
        return render_template("index.html")
    else:
        return "Erro ao cadastrar usuario"


if __name__ == "__main__":
    app.run(debug=True)

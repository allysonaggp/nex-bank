from flask import Flask, request, render_template, session, redirect, url_for
from dbapi import consultar_conta_site, inserir_registro, consultar_email
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("secret_key")  # Chave secreta para sessões


@app.route("/")
def index():
    return render_template("index.html")  # pagina de login


@app.route("/home")
def home():
    return render_template("home.html")  # pagina de login


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")  # pagina de login


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    dados = consultar_conta_site(usuario, senha)
    if dados:
        session["usuario"] = dados["nome"]
        session["conta"] = dados["id"]
        session["email"] = dados["email"]
        session["cpf"] = dados["cpf"]
        session["saldo"] = (
            f"R$: {dados['saldo']:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        session["credito"] = (
            f"R$: {dados['credito']:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        return render_template("home.html")
    else:
        return render_template("index.html", erro="Usuário ou senha incorretos")


@app.route("/cadastro", methods=["POST"])
def registrar():
    usuario = request.form["usuario"]
    email = request.form["email"]
    cpf = request.form["cpf"]
    senha = request.form["senha"]
    if consultar_email(email) == True:
        print("usuario ja existe")
        return render_template("cadastro.html", erro="Email já cadastrado")
    else:
        inserir_registro(usuario, email, cpf, senha)
        return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for("index"))  # Redireciona para a página de login


if __name__ == "__main__":
    app.run(debug=True)

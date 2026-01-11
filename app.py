from flask import Flask, request, render_template, session, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


import os
from dbapi import (
    consultar_conta_site,
    inserir_registro,
    consultar_email,
    formatar_numero_cartao,
    consultar_transacoes,
    transferir_saldo,
    consultar_id,
    inserir_registro_administrador,
    db,
)


load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("secret_key_postgres")
# app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///nexbank_local.db")

app.secret_key = os.getenv("secret_key")  # Chave secreta para sessões
db.init_app(app)


# Função iniciar
def iniciar():
    with app.app_context():
        db.create_all()
        inserir_registro_administrador("admin")
    if app.config == os.getenv("secret_key_postgres"):
        print("Servidor esta rodando Online")
    else:
        print("Servidor esta rodando Local")


@app.route("/home", methods=["GET"])
def home():
    dados = consultar_id(session["conta"])  # busca no banco
    session["saldo"] = (
        f"R$: {dados['saldo']:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
    lista_dados = consultar_transacoes(session["conta"])
    return render_template("home.html", transacoes=lista_dados)


@app.template_filter("formata_real")
def formata_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@app.route("/")
def index():
    return render_template("index.html")  # pagina de login


@app.route("/transferir")
def transferir():
    lista_dados = consultar_transacoes(session["conta"])
    return render_template(
        "transferir.html", transacoes=lista_dados
    )  # pagina de transferir




@app.route("/cadastro")
def cadastro():

    return render_template(
        "cadastro.html",
    )  # pagina de login


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    senha = request.form["senha"]

    dados = consultar_conta_site(usuario, senha)
    if dados:
        session["conta"] = dados["id"]
        session["usuario"] = dados["nome"]
        session["cpf"] = dados["cpf"]
        session["email"] = dados["email"]
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
        session["numero_cartao"] = formatar_numero_cartao(dados["numero_cartao"])
        session["validade_cartao"] = dados["validade_cartao"]
        session["chave_pix"] = dados["chave_pix"]

        lista_dados = consultar_transacoes(session["conta"])

        return render_template("home.html", transacoes=lista_dados)
    else:
        return render_template("index.html", erro="Usuário ou senha incorretos")


@app.route("/cadastro", methods=["POST"])
def registrar():
    usuario = request.form["usuario"]
    email = request.form["email"]
    cpf = request.form["cpf"]
    senha = request.form["senha"]
    if consultar_email(email):
        print("usuario ja existe")
        return render_template("cadastro.html", erro="Email já cadastrado")
    else:
        inserir_registro(usuario, email, cpf, senha)
        return render_template("index.html")


@app.route("/transacao", methods=["POST"])
def tranferir():
    usuario = consultar_id(session["conta"])
    if not usuario:
        return "Erro: Usuario não encontrado."
    descricao = request.form["descricao"]
    conta_a_receber = int(request.form["cont-number"])
    valor_a_transferir = float(request.form["valor"])
    saldo = usuario["saldo"]

    if saldo >= valor_a_transferir and saldo > 0:
        transferir_saldo(usuario["id"], conta_a_receber, valor_a_transferir, descricao, saldo)
        novo_usuario = consultar_id(session["conta"])
        session["saldo"] = f"R$: {novo_usuario['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return redirect("/home")

    else:
        print("transação nao realizada por falta de saldo")
        return render_template("transferir.html")


@app.route("/logout")
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for("index"))  # Redireciona para a página de login


if __name__ == "__main__":
    iniciar()
    app.run(debug=False)

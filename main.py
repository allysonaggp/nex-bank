import os
import getpass
from dbapi import login, inserir_registro, iniciar
from utils import limpar_tela

iniciar()

while True:
    limpar_tela()
    nome = "NexBank"
    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(f"{nome:^43}")
    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    menu = input("[1] Login\n[2] Cadastro\n[0] Sair\n")

    if menu == "1":
        limpar_tela()
        nome = "Tela de login"
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(f"{nome:^40}")
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        usuario = input("Digite seu nome de usuario: ")
        senha = getpass.getpass("Digite sua Senha: ")

        login(usuario, senha)

    elif menu == "2":
        limpar_tela()
        nome = "Tela de Cadastro"
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(f"{nome:^40}")
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        inserir_registro(
            input("\nDigite seu nome: "),
            input("Digite seu Email: "),
            getpass.getpass("Digite sua Senha: "),  # senha escondida
        )
    elif menu == "0":
        exit()
    else:
        print("Digite um número válido")
        input("Pressione Enter para continuar...")

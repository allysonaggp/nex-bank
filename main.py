import os
import getpass
from dbapi import login, inserir_registro,limpar_tela




while True:
    limpar_tela()
    nome = "Sistema de Usuarios"
    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(f"{nome:^40}")
    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    menu = input("[1] Login\n[2] Cadastro\n[0] Sair\n")
    if menu == "1":
        limpar_tela()
        nome = "Tela de login"
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(f"{nome:^40}")
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        email = input("Digite seu nome de usuario: ")
        senha = getpass.getpass("Digite sua Senha: ")

        login(email, senha)

    elif menu == "2":
        limpar_tela()
        nome = "Tela de Cadastro"
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(f"{nome:^40}")
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        inserir_registro(
            input("\nDigite seu nome: "),
            input("Digite seu Email: "),
            input("Digite sua Senha: "),
        )
    elif menu =="0":
        exit()
    else:
        print("Digite um número valido")
import getpass
import msvcrt
from dbapi import login, cadastro, iniciar, voltar_menu_login,cabecalho
from utils import limpar_tela


iniciar()

while True:
    limpar_tela()    
    cabecalho("NexBank - Seu banco digital")    

    print("[1] Login\n[2] Cadastro\n[0] Sair\n")
    menu = msvcrt.getch().decode()

    if menu == "1":
        limpar_tela()
        cabecalho("Tela de Login") 
        usuario = input("Digite seu nome de usuario: ")
        senha = getpass.getpass("Digite sua Senha: ")

        login(usuario, senha)
        voltar_menu_login()

    elif menu == "2":
        limpar_tela()
        cabecalho("Tela de Cadastro")
        cadastro()    

    elif menu == "0":
        exit()
    else:
        print("Digite um número válido")
        input("Pressione Enter para continuar...")

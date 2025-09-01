import getpass
import msvcrt
from dbapi import login, inserir_registro, iniciar, voltar_menu_login
from utils import limpar_tela


iniciar()

while True:
    limpar_tela()
    nome = "NexBank"
    linha = "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    print(linha)
    print(f"{nome:^{len(linha)}}")
    print(linha)

    print("[1] Login\n[2] Cadastro\n[0] Sair\n")
    menu = msvcrt.getch().decode()

    if menu == "1":
        limpar_tela()
        nome = "Tela de login"
        print(linha)
        print(f"{nome:^{len(linha)}}")
        print(linha)

        usuario = input("Digite seu nome de usuario: ")
        senha = getpass.getpass("Digite sua Senha: ")

        login(usuario, senha)
        voltar_menu_login()

    elif menu == "2":
        limpar_tela()
        nome = "Tela de Cadastro"
        print(linha)
        print(f"{nome:^{len(linha)}}")
        print(linha)

        nome_valido=False
        while not nome_valido:
            nome = input("\nDigite seu nome: ").strip()
            if len(nome) < 3:
                print("O nome deve ter pelo menos 3 caracteres.")
                             
            else:
                nome_valido=True

        email_valido = False
        while not email_valido:
            email = input("Digite seu Email: ").strip()
            if email.count("@") != 1 or "." not in email.split("@")[-1]:
                print("Email inválido. Tente novamente.")

            else:
                email_valido = True

        senha = getpass.getpass("Digite sua Senha: ").strip()  # senha escondida
        inserir_registro(nome, email, senha)
        voltar_menu_login()

    elif menu == "0":
        exit()
    else:
        print("Digite um número válido")
        input("Pressione Enter para continuar...")

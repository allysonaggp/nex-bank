import sqlite3
import msvcrt
import getpass
from pathlib import Path
from utils import hash_senha, limpar_tela
from datetime import datetime
from zoneinfo import ZoneInfo
import random

ROOT_PATH = Path(__file__).parent
conexao = sqlite3.connect(ROOT_PATH / "banco_de_dados.db")
cursor = conexao.cursor()


# funcao converter data UTC para local
def converter_utc_para_local(utc_str, fuso_local="America/Recife"):
    utc_dt = datetime.strptime(utc_str, "%Y-%m-%d %H:%M:%S")
    utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))
    local_dt = utc_dt.astimezone(ZoneInfo(fuso_local))
    return local_dt.strftime("%d-%m-%Y %H:%M:%S")


# Função que cria a tabela
def criar_tabela_usuarios(conexao, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100),cpf INTEGER,email VARCHAR(150),senha VARCHAR(150),saldo FLOAT,credito FLOAT,numero_cartao INTERGER,validade_cartao VARRCHAR(5),chave_pix VARCHAR(50),privilegio INTEGER)"
    )
    print("Tabela criada com Sucesso!")


# Função consultar transaçoes site
def consultar_transacoes(usuario_id):
    conn = sqlite3.connect("banco_de_dados.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM transacoes 
        WHERE origem_id = ? OR destino_id = ?
        ORDER BY data DESC
        """,
        (usuario_id, usuario_id),
    )
    transacoes = cursor.fetchall()
    conn.close()

    lista_dados = []
    for t in transacoes:
        dados = {
            "transacao": t[0],
            "origem": t[1],
            "destino": t[2],
            "descricao": t[3],
            "valor": t[4],
            "tipo": t[5],
            "data": t[6],
        }
        lista_dados.append(dados)

    return lista_dados


# Função que cria tabela transaçòes
def criar_tabela_transacoes(conexao, cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem_id INTEGER,
            destino_id INTEGER,
            descricao VARCHAR(100),
            valor FLOAT,
            tipo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (origem_id) REFERENCES usuarios(id),
            FOREIGN KEY (destino_id) REFERENCES usuarios(id)
        )
        """
    )
    conexao.commit()
    print("Tabela de transações criada com sucesso!")


# Função com verificação para cadastrar Usuário
def cadastro():

    nome_valido = False
    while not nome_valido:
        nome = input("\nDigite seu nome: ").strip()
        if len(nome) < 3:
            print("O nome deve ter pelo menos 3 caracteres.")

        else:
            nome_valido = True

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


# Formatar numero cartão
def formatar_numero_cartao(numero):
    # Remove qualquer caractere não numérico
    numero = "".join(filter(str.isdigit, str(numero)))

    # Garante que tenha 16 dígitos
    numero = numero.zfill(16)

    # Divide em blocos de 4 e junta com ponto
    blocos = [numero[i : i + 4] for i in range(0, 16, 4)]
    return ".".join(blocos)


# Funçào consultar email site
def consultar_email(email):
    data = (email,)
    # Cria conexão dentro da função
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email=?", (data))
    resultado = cursor.fetchone()

    conn.close()
    return resultado


# Funçào consultar cartao site
def consultar_cartao(cartao):
    data = (cartao,)
    # Cria conexão dentro da função
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE numero_cartao=?", (data))
    resultado = cursor.fetchone()

    conn.close()
    return resultado


#  Função pra gerar o numero do cartao de credito
def gerador_numero_cartao():
    numero = []
    for i in range(16):
        i = random.randrange(0, 9)
        numero.append(i)
    numero = "".join(str(n) for n in numero)
    # print(f'numero gerado: {numero}')
    return numero


# funcao criar cartao de credito
def criar_cartao_credito():
    verificador = False
    while verificador == False:
        numero = gerador_numero_cartao()
        if consultar_cartao(numero) == True:
            print("cartao ja cadastrado")
        else:
            # print(f'numero não cadastrado: {numero}')
            verificador = True
            print(numero)
            return numero


# Função pra cadastrar Usuário
def inserir_registro(nome, email, cpf, senha):
    senha_hash = hash_senha(senha)  # <-- aplica hash
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    cursor = conn.cursor()
    if consultar_email(email):
        print("Email já cadastrado, tente outro!")
        return
    else:
        cursor.execute("SELECT COUNT(id) FROM usuarios;")
        total_cadastrados = cursor.fetchone()[0]
        cartao = criar_cartao_credito()

        if total_cadastrados > 1 and total_cadastrados <= 5:
            data = (nome, email, cpf, senha_hash, 100, 0, 0, cartao)
        else:
            data = (nome, email, cpf, senha_hash, 0, 0, 0, cartao)

        cursor.execute(
            "INSERT INTO usuarios(nome,email,cpf,senha,saldo,credito,privilegio,numero_cartao) VALUES(?,?,?,?,?,?,?,?)",
            data,
        )
        conn.commit()
        print(f"\nusuario {nome} cadastrado com sucesso!")
        conn.close()





# Funçào consultar conta site
def consultar_conta_site(usuario, senha):
    senha_hash = hash_senha(senha)

    # Cria conexão dentro da função
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE nome=? AND senha=?", (usuario, senha_hash)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        dados = {
            "id": result[0],
            "nome": result[1],
            "cpf": result[2],
            "email": result[3],
            "saldo": result[5],
            "credito": result[6],
            "numero_cartao": result[7],
            "validade_cartao": result[8],
            "chave_pix": result[9],
        }
        return dados
    else:
        return None


# Função para cadastrar um administrador
def inserir_registro_administrador(nome, cpf, email, senha, numero_cartao, chave_pix):
    senha_hash = hash_senha(senha)
    cursor.execute("SELECT COUNT(id) FROM usuarios;")
    total_cadastrados = cursor.fetchone()[0]

    if total_cadastrados == 0:

        data = (
            nome,
            cpf,
            email,
            senha_hash,
            1,
            0,
            numero_cartao,
            0,
            chave_pix,
            "08/32",
        )
        cursor.execute(
            "INSERT INTO usuarios(nome,cpf,email,senha,privilegio,saldo,numero_cartao,credito,chave_pix,validade_cartao) VALUES(?,?,?,?,?,?,?,?,?,?)",
            data,
        )
        conexao.commit()
        print(f"\nAdministrador cadastrado com sucesso!")
    else:
        None


# Função para inserir muitos registros de uma vez
def inserir_muitos(dados):
    cursor.executemany("INSERT INTO usuarios(nome,email) Values(?,?)", dados)
    conexao.commit()
    print("\nRegistros inseridos com sucesso!\n\n")


# Função para imprimir uma linha
def linha():
    linha = "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    print(linha)


# Titulo padronizado
def cabecalho(nome):
    linha = "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    print(linha)
    print(f"{nome:^{len(linha)}}")
    print(linha)


# Iniciar
def iniciar():
    criar_tabela_usuarios(conexao, cursor)
    criar_tabela_transacoes(conexao, cursor)
    inserir_registro_administrador(
        "admin",
        "000.000.000-00",
        "admin@nexbank.com",
        "admin",
        "0000.0000.0000.0000",
        "admin@nexbank.com",
    )


# Função para atualizar dados
def atualizar_registro(nome, email, senha, id):
    data = (nome, email, senha, id)
    cursor.execute(
        "UPDATE usuarios SET nome=?, email=?,senha=? WHERE id=?",
        data,
    )
    conexao.commit()
    print(f"\nDados atualizados com sucesso!")


# Funçào consultar conta
def consultar_conta(conta):
    data = conta
    cursor.execute("SELECT * FROM usuarios Where id=?", (data,))
    conta = cursor.fetchone()
    return conta[0]


# Função para consultar registros
def consultar_registros(nome):
    data = nome
    cursor.execute("SELECT * FROM usuarios WHERE nome=?", (data,))
    result = cursor.fetchone()
    if not result:
        print("Usuario não encontrado")
    else:
        print(
            f"\nid: {result[0]} | nome: {result[1]} | email: {result[2]} | saldo: {result[5]:.2f} | credito: {result[6]:.2f}\n"
        )
        return {
            "id": result[0],
            "nome": result[1],
            "email": result[2],
            "saldo": result[5],
            "credito": result[6],
        }


# Função para consultar todos os registros
def consultar_todos_registros():
    cursor.execute("SELECT * FROM usuarios")
    results = cursor.fetchall()
    for result in results:
        print(
            f"\nid: {result[0]} | nome: {result[1]:<10} | email: {result[2]:^2} | saldo: {result[5]:<7.2f} | credito: {result[6]:.2f}"
        )


# Função consultar transaçoes
# def consultar_transacoes(usuario_id):
#     cursor.execute(
#         """
#         SELECT id, origem_id, destino_id, valor, tipo, data
#         FROM transacoes
#         WHERE origem_id = ? OR destino_id = ?
#         ORDER BY data DESC
#         """,
#         (usuario_id, usuario_id),
#     )
#     transacoes = cursor.fetchall()

#     if not transacoes:
#         nome = "Histórico de Transações:"
#         linha = "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
#         print(linha)
#         print(f"{nome:^{len(linha)}}")
#         print("\nNenhuma transação encontrada.\n")
#     else:
#         limpar_tela()
#         nome = "Histórico de Transações:"
#         linha = "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
#         print(linha)
#         print(f"{nome:^{len(linha)}}")
#         print(linha)
#         for t in transacoes:
#             print(
#                 f"Data: {converter_utc_para_local(t[5])} | Transaçao N: {t[0]} | Origem: {t[1]} | Destino: {t[2]} | Valor: {t[3]:.2f} | Tipo: {t[4]} "
#             )


# Função para voltar ao menu de login
def voltar_menu_login():
    while True:
        print("[0] Voltar ao menu principal\n")
        resposta = msvcrt.getch()
        if resposta == b"0":
            print("Voltando ao menu anterior...")
            return
        elif resposta == b"N":
            print("Ok, permanecendo no menu atual.")
        else:
            print("Opção inválida!")


# Função para login de usuarios
def login(nome, senha):
    senha_hash = hash_senha(senha)  # <-- aplica hash
    cursor.execute(
        "SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha_hash)
    )
    login = cursor.fetchone()
    if login is not None:
        # Menu Adminstrador
        if login[4] == 1:
            while True:
                limpar_tela()
                cabecalho("Sistema Administrativo - NexBank")
                print(
                    f"Conta N: {login[0]} | Saldo: {login[5]:.2f} | Credito: {login[6]:.2f}"
                )
                linha()
                print(f"\nBem vindo {login[1]}\n")
                print("[1] Gerenciador de Usuários" "\n[2] Configuraçoes\n[0] Sair\n")
                menu_principal_admin = msvcrt.getch().decode()
                # Gerenciador de Usuários
                if menu_principal_admin == "1":
                    limpar_tela()
                    cabecalho("Gerenciador de Usuários - NexBank")
                    print(f"\nBem vindo {login[1]}\n")
                    print(
                        "[1] Cadastrar Usuário\n[2] Consultar Usuário\n[3] Mostrar todos os Usuários Cadastrados\n[0] Sair\n"
                    )
                    menu_gerenciar_usuarios = msvcrt.getch().decode()
                    # Cadastrar Usuários
                    if menu_gerenciar_usuarios == "1":
                        limpar_tela()
                        cabecalho("Cadastro de Usuário - NexBank")
                        print(
                            "[1] Cadastrar Usuario\n[2] Cadastrar Administrador\n[0] Voltar ao menu principal\n"
                        )
                        menu_registro = msvcrt.getch().decode()
                        if menu_registro == "1":
                            cadastro()
                            voltar_menu_login()

                        elif menu_registro == "2":
                            inserir_registro_administrador(
                                input("\nDigite o nome do Administrador: "),
                                input("Digite o Email do Administrador: "),
                                input("Digite uma Senha para o Administrador: "),
                            )

                            voltar_menu_login()

                        elif menu_registro == "0":
                            login
                        else:
                            print("Opção invalida, tente de novo!")
                    # Consultar registro de Usuarios
                    elif menu_gerenciar_usuarios == "2":
                        limpar_tela()
                        cabecalho("Consulta de Usuário - NexBank")
                        usuario = consultar_registros(
                            input("Digite o nome do usuario que deseja consultar: ")
                        )
                        if not usuario:
                            linha()
                            voltar_menu_login()
                        else:
                            linha()
                            print(
                                f"[1] Atribuir saldo ao Usuário {usuario['nome']}\n"
                                f"[2] Atribuir credito ao Usuário {usuario['nome']}\n"
                                f"[3] Atualizar dados de {usuario['nome']}\n"
                                f"[4] Deletar conta de {usuario['nome']}\n"
                                "[0] Voltar ao menu principal\n"
                            )
                        menu = msvcrt.getch().decode()
                        # Atualizar dados do usuario
                        if menu == "1":

                            def adicionar_saldo(saldo, id):
                                data = (saldo, id)
                                cursor.execute(
                                    "UPDATE usuarios SET saldo=? WHERE id=?",
                                    data,
                                )
                                conexao.commit()
                                print(
                                    f"\nValor depositado na conta de: {usuario['nome'].upper()} com Sucesso!"
                                )

                            adicionar_saldo(
                                float(
                                    input(
                                        f"Digite o valor a ser depositado a {usuario['nome']}: \n"
                                    )
                                ),
                                usuario["id"],
                            )
                            voltar_menu_login()

                        # Atribuir credito ao usuario
                        if menu == "2":

                            def adicionar_credito(credito, id):
                                data = (credito, id)
                                cursor.execute(
                                    "UPDATE usuarios SET credito=? WHERE id=?",
                                    data,
                                )
                                conexao.commit()
                                print(
                                    f"\nValor: {usuario['credito']} Creditado na conta de: {usuario['nome'].upper()} com Sucesso!"
                                )

                            adicionar_credito(
                                float(
                                    input(
                                        f"Digite o valor a ser creditado a {usuario['nome']}: \n"
                                    )
                                ),
                                usuario["id"],
                            )
                            voltar_menu_login()

                        # Atualizar dados do usuario
                        if menu == "3":

                            def atualizar_registro_admin(
                                nome, email, senha, privilegio, id
                            ):
                                data = (
                                    nome,
                                    email,
                                    senha,
                                    privilegio,
                                    id,
                                )
                                cursor.execute(
                                    "UPDATE usuarios SET nome=?, email=?,senha=?,privilegio=? WHERE id=?",
                                    data,
                                )
                                conexao.commit()
                                print(f"\nDados atualizados com sucesso!")

                            atualizar_registro_admin(
                                input("Digite o novo Nome: "),
                                input("Digite o novo Email: "),
                                input("Digite a nova Senha: "),
                                input(
                                    "\nDigite seu Privilegio: \n"
                                    "[0] para usuario comum\n"
                                    "[1] para administrador \n"
                                ),
                                usuario["id"],
                            )
                            voltar_menu_login()

                        # Deletar conta do Usuário
                        if menu == "4":

                            def deletar_registros(id):
                                data = id
                                cursor.execute(
                                    "DELETE FROM usuarios WHERE id=?", (data,)
                                )
                                conexao.commit()
                                print("\nConta deletada com sucesso!\n\n")

                            print(
                                f"Você esta prestes a DELETAR a conta de {usuario['nome'].upper()}"
                            )
                            print("ATENÇÃO! Essa ação é irreversivel!\n")

                            print("Deseja continuar [S/N]? ")
                            confimacao = msvcrt.getch().decode().upper()
                            if confimacao == "N":
                                voltar_menu_login()
                            elif confimacao == "S" and usuario["saldo"] == 0:
                                deletar_registros(usuario["id"])
                                print("Usuário deletado com sucesso!")
                            elif confimacao == "S" and usuario["saldo"] >= 1:
                                print(
                                    "Por favor saque o dinheiro antes de deletar a conta"
                                )
                            elif confimacao == "S" and usuario["saldo"] < 0:
                                print(
                                    "Por favor pague seus debitos antes de deletar a conta"
                                )
                            else:
                                print("Opção invalida, tente de novo!")

                            voltar_menu_login()
                        # Sair
                        if menu == 0:
                            voltar_menu_login()
                        else:
                            print("Digite uma opção válida")

                    # Todos os Usuários cadastrados
                    elif menu_gerenciar_usuarios == "3":
                        limpar_tela()
                        cabecalho("Todos os Usuários Cadastrados - NexBank")
                        consultar_todos_registros()
                        linha()
                        voltar_menu_login()

                # Configurações
                elif menu_principal_admin == "2":
                    limpar_tela()
                    cabecalho("Configurações de conta - NexBank")
                    print(
                        "[1] Modificar dados do cadastro \n[2] Deletar Conta \n[0] Sair\n"
                    )
                    menu = msvcrt.getch().decode()
                    # Mudar dados do Cadastro
                    if menu == "1":
                        limpar_tela()
                        cabecalho("Atualizar dados de Usuario - NexBank")

                        print(
                            "[1] Atualizar Nome\n[2] Atualizar Email\n[3] Atualizar Senha\n[0] Sair\n"
                        )
                        menu_atualizar_dados = msvcrt.getch().decode()

                        # Padrão para atualizar nome
                        if menu_atualizar_dados == "1":
                            nome_valido = False
                            while not nome_valido:
                                nome = input("\nDigite seu nome: ").strip()
                                if len(nome) < 3:
                                    print("O nome deve ter pelo menos 3 caracteres.")
                                else:
                                    nome_valido = True

                            atualizar_registro(
                                nome,
                                login[2],
                                login[3],
                                login[0],
                            )
                            voltar_menu_login()

                        # Padrão para atualizar email
                        if menu_atualizar_dados == "2":
                            email_valido = False
                            while not email_valido:
                                email = input("Digite seu Email: ").strip()
                                if (
                                    email.count("@") != 1
                                    or "." not in email.split("@")[-1]
                                ):
                                    print("Email inválido. Tente novamente.")

                                else:
                                    email_valido = True

                            atualizar_registro(
                                login[1],
                                email,
                                login[3],
                                login[0],
                            )
                            voltar_menu_login()

                        # Padrão para atualizar senha
                        if menu_atualizar_dados == "3":
                            senha_valida = False
                            while not senha_valida:
                                senha = input("Digite sua Senha: ").strip()
                                senha2 = input("Confirme sua Senha: ").strip()
                                if senha != senha2:
                                    print("Senhas não conferem, tente novamente.")
                                else:
                                    senha_valida = True
                            senha_hash = hash_senha(senha)
                            atualizar_registro(
                                login[1],
                                login[2],
                                senha_hash,
                                login[0],
                            )
                            voltar_menu_login()

                        # Sair
                        if menu_atualizar_dados == "0":

                            voltar_menu_login()

                    # Deletar conta do Usuário
                    elif menu == "2":
                        limpar_tela()
                        cabecalho("Deletar conta de Usuario - NexBank")

                        def deletar_registros(id):
                            data = (id,)
                            cursor.execute("DELETE FROM usuarios WHERE id=?", (data))
                            conexao.commit()
                            print("\nConta deletada com sucesso!\n\n")

                        print("ATENÇÃO! Essa ação é irreversivel!\n")

                        print("Deseja continuar [S/N]? ")
                        confimacao = msvcrt.getch().decode().upper()
                        if confimacao == "N":
                            login
                        elif confimacao == "S":
                            deletar_registros(login[0])
                            break
                        else:
                            print("Opção invalida, tente de novo!")
                # Sair
                elif menu_principal_admin == "0":
                    print("Saindo...")
                    break

                else:
                    print("Opção invalida, tente de novo!")

        # menu do Usuário
        elif login[4] == 0:

            while True:
                limpar_tela()
                cabecalho("NexBank - Seu banco digital")
                print(
                    f"Conta N: {login[0]} | Saldo: {login[5]:.2f} | Credito: {login[6]:.2f}"
                )
                linha()
                print(f"\nBem vindo {login[1]}")

                print("\n[1] Transações\n[2] Configuraçoes\n[0] Sair\n")
                menu_principal = msvcrt.getch().decode()
                # Area de Credito Bancario
                if menu_principal == "1":
                    limpar_tela()
                    cabecalho("Transações - NexBank")
                    print(
                        f"Conta N: {login[0]} | Saldo: {login[5]:.2f} | Credito: {login[6]:.2f}"
                    )

                    print(
                        "\n[1] Transferência\n[2] Ver histórico de transações\n[0] Voltar ao menu principal\n"
                    )
                    menu_transacoes = msvcrt.getch().decode()
                    # Transferência
                    if menu_transacoes == "1":
                        limpar_tela()
                        nome = "Transações"
                        cabecalho("Transações - NexBank")
                        print(
                            f"Conta N: {login[0]} | Saldo: {login[5]:.2f} | Credito: {login[6]:.2f}"
                        )
                        linha()
                        verificador_conta = False
                        while verificador_conta is False:
                            conta_a_receber = consultar_conta(
                                input("Digite o número da conta que irá receber: ")
                            )
                            if not conta_a_receber:
                                print("Conta nao encontrada\n")
                            elif conta_a_receber == login[0]:
                                print(
                                    "Por favor digite outra conta você nao pode transferir para você mesmo\n"
                                )
                            else:
                                verificador_conta = True
                                valor_a_transferir = float(input("digite o valor: "))

                                if login[5] >= valor_a_transferir:
                                    # debita
                                    cursor.execute(
                                        "UPDATE usuarios SET saldo = saldo - ? WHERE id=?",
                                        (valor_a_transferir, login[0]),
                                    )
                                    # credita
                                    cursor.execute(
                                        "UPDATE usuarios SET saldo = saldo + ? WHERE id=?",
                                        (valor_a_transferir, conta_a_receber),
                                    )
                                    # registra transação
                                    cursor.execute(
                                        "INSERT INTO transacoes (origem_id, destino_id, valor, tipo) VALUES (?, ?, ?, ?)",
                                        (
                                            login[0],
                                            conta_a_receber,
                                            valor_a_transferir,
                                            "transferencia",
                                        ),
                                    )
                                    conexao.commit()
                                    print("Transferência realizada com sucesso!")
                                else:
                                    print("Saldo insuficiente!")

                        voltar_menu_login()
                    # Histórico de transações
                    if menu_transacoes == "2":
                        limpar_tela()
                        consultar_transacoes(login[0])
                        linha()
                        voltar_menu_login()
                    # Sair
                    elif menu_transacoes == "0":
                        voltar_menu_login()
                    else:
                        print("digite um numero válido!")

                # Configurações
                elif menu_principal == "2":
                    limpar_tela()
                    cabecalho("Configurações de conta - NexBank")
                    print(
                        "[1] Modificar dados do cadastro \n[2] Deletar Conta \n[0] Sair\n"
                    )
                    menu = msvcrt.getch().decode()
                    # Mudar dados do Cadastro
                    if menu == "1":
                        limpar_tela()
                        cabecalho("Atualizar dados de Usuario - NexBank")

                        print(
                            "[1] Atualizar Nome\n[2] Atualizar Email\n[3] Atualizar Senha\n[0] Sair\n"
                        )
                        menu_atualizar_dados = msvcrt.getch().decode()

                        # Padrão para atualizar nome
                        if menu_atualizar_dados == "1":
                            nome_valido = False
                            while not nome_valido:
                                nome = input("\nDigite seu nome: ").strip()
                                if len(nome) < 3:
                                    print("O nome deve ter pelo menos 3 caracteres.")
                                else:
                                    nome_valido = True

                            atualizar_registro(
                                nome,
                                login[2],
                                login[3],
                                login[0],
                            )
                            voltar_menu_login()

                        # Padrão para atualizar email
                        if menu_atualizar_dados == "2":
                            email_valido = False
                            while not email_valido:
                                email = input("Digite seu Email: ").strip()
                                if (
                                    email.count("@") != 1
                                    or "." not in email.split("@")[-1]
                                ):
                                    print("Email inválido. Tente novamente.")

                                else:
                                    email_valido = True

                            atualizar_registro(
                                login[1],
                                email,
                                login[3],
                                login[0],
                            )
                            voltar_menu_login()

                        # Padrão para atualizar senha
                        if menu_atualizar_dados == "3":
                            senha_valida = False
                            while not senha_valida:
                                senha = input("Digite sua Senha: ").strip()
                                senha2 = input("Confirme sua Senha: ").strip()
                                if senha != senha2:
                                    print("Senhas não conferem, tente novamente.")
                                else:
                                    senha_valida = True
                            senha_hash = hash_senha(senha)
                            atualizar_registro(
                                login[1],
                                login[2],
                                senha_hash,
                                login[0],
                            )
                            voltar_menu_login()

                        # Sair
                        if menu_atualizar_dados == "0":

                            voltar_menu_login()

                    # Deletar conta do Usuário
                    elif menu == "2":
                        limpar_tela()
                        cabecalho("Deletar conta de Usuario - NexBank")

                        def deletar_registros(id):
                            data = (id,)
                            cursor.execute("DELETE FROM usuarios WHERE id=?", (data))
                            conexao.commit()
                            print("\nConta deletada com sucesso!\n\n")

                        print("ATENÇÃO! Essa ação é irreversivel!\n")

                        print("Deseja continuar [S/N]? ")
                        confimacao = msvcrt.getch().decode().upper()
                        if confimacao == "N":
                            login
                        elif confimacao == "S" and login[5] == 0:
                            deletar_registros(login[0])
                            break
                        elif confimacao == "S" and login[5] >= 1:
                            print("Por favor saque o dinheiro antes de deletar a conta")
                            voltar_menu_login()
                        elif confimacao == "S" and login[5] < 0:
                            print(
                                "Por favor pague seus debitos antes de deletar a conta"
                            )
                            voltar_menu_login()
                        else:
                            print("Opção invalida, tente de novo!")

                # Sair
                elif menu_principal == "0":
                    print("Saindo...")
                    break

                else:
                    print("Opção invalida, tente de novo!")

        # Usuário não autorizado
        else:
            print("\nUsuário nao autorizado!\n\n")
    # Usuário ou senha invalidos
    else:
        print("Usuário ou senha invalidos")

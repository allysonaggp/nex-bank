import sqlite3
from pathlib import Path
from utils import hash_senha, limpar_tela

ROOT_PATH = Path(__file__).parent
conexao = sqlite3.connect(ROOT_PATH / "banco_de_dados.db")
cursor = conexao.cursor()


# Função que cria a tabela
def criar_tabela_usuarios(conexao, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100),email VARCHAR(150),senha VARCHAR(150),privilegio iNTEGER,saldo REAL,credito REAL)"
    )
    print("Tabela criada com Sucesso!")


# Função que cria tabela transaçòes
def criar_tabela_transacoes(conexao, cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem_id INTEGER,
            destino_id INTEGER,
            valor REAL,
            tipo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (origem_id) REFERENCES usuarios(id),
            FOREIGN KEY (destino_id) REFERENCES usuarios(id)
        )
        """
    )
    conexao.commit()
    print("Tabela de transações criada com sucesso!")


# Função pra cadastrar Usuário
def inserir_registro(nome, email, senha):
    senha_hash = hash_senha(senha)  # <-- aplica hash
    cursor.execute("SELECT COUNT(id) FROM usuarios;")
    total_cadastrados = cursor.fetchone()[0]

    if total_cadastrados <= 10:
        data = (nome, email, senha_hash, 100, 0, 0)
    else:
        data = (nome, email, senha_hash, 0, 0, 0)

    cursor.execute(
        "INSERT INTO usuarios(nome,email,senha,saldo,credito,privilegio) VALUES(?,?,?,?,?,?)",
        data,
    )
    conexao.commit()
    print(f"\nusuario {nome} cadastrado com sucesso!")


# Função para cadastrar um administrador
def inserir_registro_administrador(nome, email, senha):
    data = (nome, email, senha, 1)
    cursor.execute(
        "INSERT INTO usuarios(nome,email,senha,privilegio) VALUES(?,?,?,?)", data
    )
    conexao.commit()
    print(f"\nAdministrador cadastrado com sucesso!")


# iniciar
def iniciar():
    criar_tabela_usuarios(conexao, cursor)
    criar_tabela_transacoes(conexao, cursor)
    # inserir_registro_administrador("admin", "admin@gmail", "admin")


# Função para inserir muitos registros de uma vez
def inserir_muitos(dados):
    cursor.executemany("INSERT INTO usuarios(nome,email) Values(?,?)", dados)
    conexao.commit()
    print("\nRegistros inseridos com sucesso!\n\n")


# Função para consultar registros
def consultar_registros(nome):
    data = nome
    cursor.execute("SELECT * FROM usuarios WHERE nome=?", (data,))
    result = cursor.fetchone()
    if result:
        print(f"\nid: {result[0]:<4} nome: {result[1]:<20} email: {result[2]}")
        return {
            "id": result[0],
            "nome": result[1],
            "email": result[2],
            "saldo": result[5],
            "credito": result[6],
        }
    else:
        print("Usuario não encontrado")


# Função consultar transaçoes
def consultar_transacoes(usuario_id):
    cursor.execute(
        """
        SELECT id, origem_id, destino_id, valor, tipo, data 
        FROM transacoes 
        WHERE origem_id = ? OR destino_id = ?
        ORDER BY data DESC
        """,
        (usuario_id, usuario_id),
    )
    transacoes = cursor.fetchall()

    if not transacoes:
        print("\nNenhuma transação encontrada.\n")
    else:
        limpar_tela()
        nome = "Histórico de Transações:"
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print(f"{nome:^42}")
        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        for t in transacoes:
            print(
                f"ID: {t[0]} | Origem: {t[1]} | Destino: {t[2]} | Valor: {t[3]:.2f}\nTipo: {t[4]} | Data: {t[5]}\n"
                "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
            )


# Função para consultar todos os registros
def consultar_todos_registros():
    cursor.execute("SELECT * FROM usuarios")
    results = cursor.fetchall()
    for result in results:
        print(f"id: {result[0]:<4} nome: {result[1]:<20} email: {result[2]}")


# Função para voltar ao menu de login
def voltar_menu_login():
    while True:
        resposta = input("[0] Voltar ao menu principal\n").strip().upper()
        if resposta == "0":
            print("Voltando ao menu anterior...")
            return
        elif resposta == "N":
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
                nome = "Sistema do administrador"
                print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                print(f"{nome:^40}")
                print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                print(f"\nBem vindo {login[1]}\n")
                menu_principal_admin = input(
                    "[1] Gerenciador de Usuários" "\n[2] Configuraçoes\n[0] Sair\n"
                )
                # Gerenciador de Usuários
                if menu_principal_admin == "1":
                    limpar_tela()
                    nome = "Gerenciador de Usuários"
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f"{nome:^40}")
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f"\nBem vindo {login[1]}\n")
                    menu_gerenciar_usuarios = input(
                        "[1] Cadastrar Usuário"
                        "\n[2] Consultar Usuário\n[3] Mostrar todos os Usuários Cadastrados\n[0] Sair\n"
                    )
                    # Cadastrar Usuários
                    if menu_gerenciar_usuarios == "1":
                        limpar_tela()
                        nome = "Cadastrar Usuários"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^40}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        menu_registro = input(
                            "[1] Cadastrar Usuario\n[2] Cadastrar Administrador\n[0] Voltar ao menu principal\n"
                        )
                        if menu_registro == "1":
                            inserir_registro(
                                input("\nDigite o seu nome: "),
                                input("Digite o seu Email: "),
                                input("Digite uma Senha: "),
                            )
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
                        nome = "Consultar registro de Usuarios"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^50}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        usuario = consultar_registros(
                            input("Digite o nome do usuario que deseja consultar: ")
                        )
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

                        menu = input(
                            f"[1] Atribuir saldo ao Usuário {usuario['nome']}\n"
                            f"[2] Atribuir credito ao Usuário {usuario['nome']}\n"
                            f"[3] Atualizar dados de {usuario['nome']}\n"
                            f"[4] Deletar conta de {usuario['nome']}\n"
                            "[0] Voltar ao menu principal\n"
                        )
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
                                input(
                                    f"Digite o valor a ser depositado no Usuário: {usuario['nome']}\n"
                                ),
                                usuario["id"],
                            )
                            voltar_menu_login()
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
                                input(
                                    f"Digite o valor do credito do Usuário: {usuario['nome']}\n"
                                ),
                                usuario["id"],
                            )
                            voltar_menu_login()
                        if menu == "3":

                            def atualizar_registro(nome, email, senha, privilegio, id):
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

                            atualizar_registro(
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

                            confimacao = (
                                input("Deseja continuar [S/N]? ").strip().upper()[0]
                            )
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

                        if menu == 0:
                            voltar_menu_login()
                        else:
                            print("Digite uma opção válida")

                    # Todos os Usuários cadastrados
                    elif menu_gerenciar_usuarios == "3":
                        limpar_tela()
                        nome = "Todos Usuarios cadastrados"
                        print(
                            "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-"
                        )
                        print(f"{nome:^60}")
                        print(
                            "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-"
                        )
                        consultar_todos_registros()
                        print(
                            "=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-"
                        )
                        voltar_menu_login()

                # Configurações
                elif menu_principal_admin == "2":
                    limpar_tela()
                    nome = "Configurações"
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f"{nome:^42}")
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    menu = input(
                        "[1] Modificar dados do cadastro \n[2] Deletar Conta \n[0] Sair\n"
                    )
                    # Mudar dados do Cadastro
                    if menu == "1":
                        limpar_tela()
                        nome = "Atualizar dados de Usuario"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^42}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

                        def atualizar_registro(nome, email, senha, id):
                            data = (nome, email, senha, id)
                            cursor.execute(
                                "UPDATE usuarios SET nome=?, email=?,senha=? WHERE id=?",
                                data,
                            )
                            conexao.commit()
                            print(f"\nDados atualizados com sucesso!")

                        atualizar_registro(
                            input("Digite o novo Nome: "),
                            input("Digite o novo Email: "),
                            input("Digite a nova Senha: "),
                            login[0],
                        )
                        voltar_menu_login()

                    # Deletar conta do Usuário
                    elif menu == "2":
                        limpar_tela()
                        nome = "Deletar conta de Usuario"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^42}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

                        def deletar_registros(id):
                            data = (id,)
                            cursor.execute("DELETE FROM usuarios WHERE id=?", (data))
                            conexao.commit()
                            print("\nConta deletada com sucesso!\n\n")

                        print("ATENÇÃO! Essa ação é irreversivel!\n")

                        confimacao = (
                            input("Deseja continuar [S/N]? ").strip().upper()[0]
                        )
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
                nome = "NexBank"
                print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                print(f"{nome:^43}")
                print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                print(
                    f"Saldo: {login[5]:.2f}                   Conta N: {login[0]}\n"
                    f"Credito: {login[6]:.2f}"
                )
                print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                print(f"\nBem vindo {login[1]}")

                menu_principal = input(
                    "\n[1] Transações\n[2] Configuraçoes\n[0] Sair\n"
                )
                # Area de Credito Bancario
                if menu_principal == "1":
                    limpar_tela()
                    nome = "Transações"
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f"{nome:^40}")
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f"Conta N: {login[0]}\n")
                    print(f"Saldo: {login[5]:.2f} Credito: {login[6]:.2f}")

                    menu_transacoes = input(
                        "\n[1] Transferência\n[2] Ver histórico de transações\n[0] Voltar ao menu principal\n"
                    )

                    if menu_transacoes == "1":
                        limpar_tela()
                        nome = "Transações"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^40}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"Conta N: {login[0]}\n")
                        print(f"Saldo: {login[5]:.2f} Credito: {login[6]:.2f}\n")

                        conta_a_receber = int(input("Digite o numero da conta: "))
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

                    if menu_transacoes == "2":
                        limpar_tela()
                        consultar_transacoes(login[0])
                        voltar_menu_login()

                    elif menu_transacoes == "0":
                        voltar_menu_login()
                    else:
                        print("digite um numero válido!")

                # configurações
                if menu_principal == "2":
                    limpar_tela()
                    nome = "Configurações"
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f"{nome:^42}")
                    print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    menu_configuracoes = input(
                        "[1] Modificar dados do cadastro \n[2] Deletar Conta \n[0] Sair\n"
                    )

                    # Mudar dados do Cadastro
                    if menu_configuracoes == "1":
                        limpar_tela()
                        nome = "Atualizar dados de Usuario"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^42}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"id: {login[0]} e nome: {login[1]}")

                        def atualizar_registro(nome, email, senha, id):
                            data = (nome, email, senha, id)
                            cursor.execute(
                                "UPDATE usuarios SET nome=?, email=?,senha=? WHERE id=?",
                                data,
                            )
                            conexao.commit()
                            print(f"\nDados atualizados com sucesso!")

                        atualizar_registro(
                            input("Digite o novo Nome: "),
                            input("Digite o novo Email: "),
                            input("Digite a nova Senha: "),
                            login[0],
                        )
                        voltar_menu_login()

                    # Deletar conta do Usuário
                    elif menu_configuracoes == "2":
                        limpar_tela()
                        nome = "Deletar conta de Usuario"
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                        print(f"{nome:^42}")
                        print("=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

                        def deletar_registros(id):
                            data = (id,)
                            cursor.execute("DELETE FROM usuarios WHERE id=?", (data))
                            conexao.commit()
                            print("\nConta deletada com sucesso!\n\n")

                        print("ATENÇÃO! Essa ação é irreversivel!\n")

                        confimacao = (
                            input("Deseja continuar [S/N]? ").strip().upper()[0]
                        )
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

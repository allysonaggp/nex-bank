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
    return local_dt.strftime("%d-%m-%Y as %H:%M")


# Função que cria a tabela
def criar_tabela_usuarios(conexao, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100),cpf VARCHAR(9),email VARCHAR(150),senha VARCHAR(150),saldo FLOAT,credito FLOAT,numero_cartao INTERGER,validade_cartao VARRCHAR(5),chave_pix VARCHAR(50),privilegio INTEGER)"
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
            descricao TEXT,
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


# Função consultar transaçoes site
def consultar_transacoes(minha_conta):
    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, origem_id, destino_id, descricao, valor, tipo, data
        FROM transacoes
        WHERE origem_id = ? OR destino_id = ?
        ORDER BY data DESC
    """,
        (minha_conta, minha_conta),
        
    )

    resultado = cursor.fetchall()
    conexao.close()

    transacoes_formatadas = []
    for t in resultado:
        id_transacao, origem, destino, descricao, valor, tipo, data = t

        # Se eu sou o destino, recebi dinheiro → positivo
        # Se eu sou a origem, enviei dinheiro → negativo
        valor_num = valor if destino == minha_conta else -valor

        transacoes_formatadas.append(
            {
                "transacao": id_transacao,
                "origem": origem,
                "destino": destino,
                "descricao": descricao,
                "valor_num": valor_num,  # ← esse campo é calculado aqui!
                "valor": f"R$: {abs(valor_num):,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", "."),
                "tipo": tipo,
                "data": converter_utc_para_local(data),
            }
        )

    return transacoes_formatadas


# Função transferir
def transferir_saldo(conta, conta_a_receber, valor_a_transferir, descricao, saldo):

    conexao = sqlite3.connect("banco_de_dados.db")
    cursor = conexao.cursor()

    verificador_conta = False
    while verificador_conta is False:
        conta_a_receber = consultar_conta(conta_a_receber)

        if not conta_a_receber:
            print("Conta nao encontrada\n")
        elif conta_a_receber == conta:
            print(
                "Por favor digite outra conta você nao pode transferir para você mesmo\n"
            )
        elif saldo >= valor_a_transferir:
            verificador_conta = True
            # debita
            cursor.execute(
                "UPDATE usuarios SET saldo = saldo - ? WHERE id=?",
                (valor_a_transferir, conta),
            )
            # credita
            cursor.execute(
                "UPDATE usuarios SET saldo = saldo + ? WHERE id=?",
                (valor_a_transferir, conta_a_receber),
            )
            # registra transação
            cursor.execute(
                "INSERT INTO transacoes (origem_id, destino_id, valor,descricao, tipo) VALUES (?, ?, ?, ?, ?)",
                (
                    conta,
                    conta_a_receber,
                    valor_a_transferir,
                    descricao,
                    "transferencia",
                ),
            )
            conexao.commit()
            conexao.close()


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
def consultar_site(id):
    data = (id,)
    # Cria conexão dentro da função
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id=?", (data))
    dados = cursor.fetchone()
    dados = {
        "id": dados[0],
        "nome": dados[1],
        "cpf": dados[2],
        "email": dados[3],
        "saldo": dados[5],
        "credito": dados[6],
        "numero_cartao": dados[7],
        "validade_cartao": dados[8],
        "chave_pix": dados[9],
    }

    return dados


# Funçào consultar cartao site
def consultar_id(id):
    data = (id,)
    # Cria conexão dentro da função
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id=?", (data))
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
        validade_cartao = "09/32"
        if total_cadastrados > 1 and total_cadastrados <= 5:
            data = (nome, email, cpf, senha_hash, 100, 0, 0, cartao, validade_cartao)
        else:
            data = (nome, email, cpf, senha_hash, 0, 0, 0, cartao, validade_cartao)

        cursor.execute(
            "INSERT INTO usuarios(nome,email,cpf,senha,saldo,credito,privilegio,numero_cartao,validade_cartao) VALUES(?,?,?,?,?,?,?,?,?)",
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
        "SELECT * FROM usuarios WHERE email=? AND senha=?", (usuario, senha_hash)
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
    conn = sqlite3.connect("banco_de_dados.db", check_same_thread=False)
    cursor = conn.cursor()
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

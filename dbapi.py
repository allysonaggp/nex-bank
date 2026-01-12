from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
import random


db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.Text)
    email = db.Column(db.String(150))
    senha = db.Column(db.Text)
    saldo = db.Column(db.Float)
    credito = db.Column(db.Float)
    numero_cartao = db.Column(db.Text)
    validade_cartao = db.Column(db.String(5))
    chave_pix = db.Column(db.String(50))
    privilegio = db.Column(db.Integer)
    data = db.Column(db.DateTime, default=datetime.utcnow)


class Transacao(db.Model):
    __tablename__ = "transacoes"
    id = db.Column(db.Integer, primary_key=True)
    origem_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    destino_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    descricao = db.Column(db.Text)
    valor = db.Column(db.Float)
    tipo = db.Column(db.String)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    origem = db.relationship(
        "Usuario", foreign_keys=[origem_id], backref="transacoes_enviadas"
    )
    destino = db.relationship(
        "Usuario", foreign_keys=[destino_id], backref="transacoes_recebidas"
    )


# funcao converter data UTC para local
def converter_utc_para_local(utc_value, fuso_local="America/Sao_Paulo"):
    # Se já for datetime, usa direto
    if isinstance(utc_value, datetime):
        utc_dt = utc_value
    else:  # se for string, faz o parse
        utc_dt = datetime.strptime(utc_value, "%d-%m-%Y às %H:%M")

    # garantir que está em UTC
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))

    # converte para o fuso desejado
    local_dt = utc_dt.astimezone(ZoneInfo(fuso_local))

    # retorna como string formatada
    return local_dt.strftime("%d-%m-%Y às %H:%M")



# Formatar numero cartão
def formatar_numero_cartao(numero):
    # Remove qualquer caractere não numérico
    numero = "".join(filter(str.isdigit, str(numero)))

    # Garante que tenha 16 dígitos
    numero = numero.zfill(16)

    # Divide em blocos de 4 e junta com ponto
    blocos = [numero[i : i + 4] for i in range(0, 16, 4)]
    return ".".join(blocos)


# Funções de acesso ao banco
def consultar_conta_site(email, senha):
    user = Usuario.query.filter_by(email=email).first()
    if user and check_password_hash(user.senha, senha):
        return {
            "id": user.id,
            "nome": user.nome,
            "cpf": user.cpf,
            "email": user.email,
            "saldo": user.saldo,
            "credito": user.credito,
            "numero_cartao": user.numero_cartao,
            "validade_cartao": user.validade_cartao,
            "chave_pix": user.chave_pix,
        }
    return None


# Funçào consultar cartao site
def consultar_cartao(cartao):
    usuario = Usuario.query.filter_by(numero_cartao=cartao).first()
    return usuario


#  Função pra gerar o numero do cartao de credito
def gerador_numero_cartao():
    numero = []
    for i in range(16):
        numero.append(random.randint(0, 9))
    numero = "".join(str(n) for n in numero)
    # print(f'numero gerado: {numero}')
    return numero


# funcao criar cartao de credito
def criar_cartao_credito():
    verificador = False
    while verificador == False:
        numero = gerador_numero_cartao()
        if consultar_cartao(numero):
            print("cartao ja cadastrado")
        else:
            # print(f'numero não cadastrado: {numero}')
            verificador = True
            print(numero)
            return numero


# Funcao cadastrar usuario
def inserir_registro(nome, email, cpf, senha):
    if Usuario.query.filter_by(email=email).first():
        print("Email já cadastrado, tente outro!")
        return

    total_cadastrados = Usuario.query.count()
    cartao = criar_cartao_credito()
    validade_cartao = "09/32"
    senha_hash = generate_password_hash(senha)

    credito_inicial = 100 if total_cadastrados <= 300 else 0

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        cpf=cpf,
        senha=senha_hash,
        saldo=credito_inicial,
        credito=0,
        privilegio=0,
        numero_cartao=cartao,
        validade_cartao=validade_cartao,    
    )

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        print(f"\nUsuário {nome} cadastrado com sucesso!")
    except IntegrityError:
        db.session.rollback()
        print("Erro ao cadastrar usuário. Verifique os dados e tente novamente.")


# Função para cadastrar um administrador
def inserir_registro_administrador(senha):
    senha_hash = generate_password_hash(senha)

    # Verifica se já existe algum usuário cadastrado
    total_cadastrados = db.session.query(Usuario).count()

    if total_cadastrados == 0:
        novo_admin = Usuario(
            nome="admin",
            cpf="00000000000",
            email="admin@nexbank.com",
            senha=senha_hash,
            saldo=150000,
            credito=10000,
            numero_cartao="4567365496731746",
            validade_cartao="08/32",
            chave_pix="admin@nexbank.com",
            privilegio=1,
        )

        db.session.add(novo_admin)
        db.session.commit()
        print("\n✅ Administrador cadastrado com sucesso!")
    else:
        print("\nℹ️ Já existe um usuário cadastrado.")


# Função transferir
def transferir_saldo(
    conta_id, conta_a_receber_id, valor_a_transferir, descricao, saldo
):
    verificador_conta = False

    while not verificador_conta:
        conta_destino = Usuario.query.get(conta_a_receber_id)

        if not conta_destino:
            print("Conta não encontrada\n")
            return

        if conta_a_receber_id == conta_id:
            print(
                "Por favor digite outra conta. Você não pode transferir para você mesmo\n"
            )
            return

        if saldo >= valor_a_transferir:
            verificador_conta = True

            # Debita da conta de origem
            conta_origem = Usuario.query.get(conta_id)
            conta_origem.saldo -= valor_a_transferir

            # Credita na conta de destino
            conta_destino.saldo += valor_a_transferir

            # Registra transação
            transacao = Transacao(
                origem_id=conta_id,
                destino_id=conta_a_receber_id,
                valor=valor_a_transferir,
                descricao=descricao,
                tipo="transferencia",
            )

            try:
                db.session.add(transacao)
                db.session.commit()
                print("Transferência realizada com sucesso!")
            except Exception as e:
                db.session.rollback()
                print("Erro ao realizar transferência:", str(e))


# Funcao consultar id
def consultar_id(id):
    user = Usuario.query.get(id)
    usuario = {
        "id": user.id,
        "nome": user.nome,
        "cpf": user.cpf,
        "email": user.email,
        "saldo": user.saldo,
        "credito": user.credito,
        "numero_cartao": user.numero_cartao,
        "validade_cartao": user.validade_cartao,
        "chave_pix": user.chave_pix,
    }

    return usuario


# Funcao consultar email
def consultar_email(email):
    usuario = Usuario.query.filter_by(email=email).first()
    return usuario


# Função consultar transaçoes site
def consultar_transacoes(minha_conta):
    transacoes = (
        Transacao.query.filter(
            or_(Transacao.origem_id == minha_conta, Transacao.destino_id == minha_conta)
        )
        .order_by(Transacao.data.desc())
        .all()
    )

    transacoes_formatadas = []
    for t in transacoes:
        valor_num = t.valor if t.destino_id == minha_conta else -t.valor

        transacoes_formatadas.append(
            {
                "transacao": t.id,
                "origem": t.origem_id,
                "destino": t.destino_id,
                "descricao": t.descricao,
                "valor_num": valor_num,
                "valor": f"R$: {abs(valor_num):,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", "."),
                "tipo": t.tipo,
                "data": converter_utc_para_local(t.data),
            }
        )

    return transacoes_formatadas

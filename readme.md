# 🏦 NexBank

**NexBank** é um sistema bancário em **Python**, que simula funcionalidades de um banco real, incluindo cadastro, login, gerenciamento de usuários, transações financeiras e histórico de movimentações.

O sistema utiliza **SQLite** para persistência de dados e implementa **hash de senhas** para segurança.

---

## 🚀 Funcionalidades

### Para Usuários Comuns

* ✅ Cadastro de conta com nome, e-mail e senha(criptografada).
* ✅ Login seguro com autenticação de senha.
* ✅ Consultar saldo e crédito disponíveis.
* ✅ Realizar transferências entre contas.
* ✅ Consultar histórico de transações.
* ✅ Atualizar dados pessoais.
* ✅ Deletar a própria conta (saldo deve ser 0).

### Para Administradores

* ✅ Cadastrar usuários e administradores.
* ✅ Consultar dados de qualquer usuário.
* ✅ Atribuir saldo ou crédito a usuários.
* ✅ Atualizar dados de usuários.
* ✅ Deletar contas de usuários (verificando saldo/credito).
* ✅ Visualizar todos os usuários cadastrados.

---

## 📂 Estrutura do Projeto

```
NexBank/
│
├─ main.py            # Interface principal do usuário e menu
├─ dbapi.py           # Funções de acesso ao banco de dados
├─ utils.py           # Funções utilitárias (limpar tela, hash de senha)
├─ banco_de_dados.db  # Banco de dados SQLite
└─ README.md          # Este arquivo
```

---

## 🛠 Tecnologias

* Python 3.x
* SQLite
* Biblioteca `hashlib` para hash de senhas

---

## ⚡ Como Rodar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/NexBank.git
```

2. Acesse a pasta do projeto:

```bash
cd NexBank
```

3. Execute o arquivo principal:

```bash
python main.py
```

4. Use o menu para login, cadastro ou acessar funcionalidades de administrador.

---

## 🔒 Segurança

* Senhas armazenadas em **hash SHA-256**, garantindo que não fiquem em texto plano no banco de dados.

---

## 🧑‍💻 Primeiro Administrador

O primeiro administrador é criado automaticamente com os seguintes dados:

* **Nome:** admin
* **Email:** admin\@nexbank.com
* **Senha:** admin

> ⚠️ Recomenda-se alterar a senha do administrador após o primeiro login.

---

## 📸 Exemplos de Telas

### Menu Inicial
```
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                              NexBank - Seu banco digital
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
[1] Login
[2] Cadastro
[0] Sair
```



---

### Tela de Login
```
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                     Tela de Login
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Digite seu nome de usuario: admin
Digite sua Senha: 
```



---

### Tela de Usuário
```
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                              NexBank - Seu banco digital
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Conta N: 2 | Saldo: 100.00 | Credito: 0.00
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Bem vindo maycon

[1] Transações
[2] Configuraçoes
[0] Sair
```



---

### Tela de Adminstrador
```
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                           Sistema Administrativo - NexBank
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Conta N: 1 | Saldo: 0.00 | Credito: 0.00
=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Bem vindo admin

[1] Gerenciador de Usuários
[2] Configuraçoes
[0] Sair
```



---

## 📌 Observações

* Para deletar uma conta, o saldo do usuário deve ser 0.
* Apenas administradores podem acessar funções de gerenciamento de outros usuários.

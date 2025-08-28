# 📌 Sistema de Usuários em Python + SQLite

Este é um sistema de gerenciamento de usuários em **Python** utilizando **SQLite3** como banco de dados.  
O sistema possui dois tipos de usuários: **administrador** e **usuário comum**.

## 🚀 Funcionalidades

- [x] Cadastro de usuários
- [x] Cadastro de administradores
- [x] Login com autenticação
- [x] Menu diferenciado para usuários e administradores
- [x] Atualizar dados de cadastro
- [x] Excluir conta
- [x] Consultar usuários (apenas administradores)
- [x] Listar todos os usuários cadastrados
- [ ] Cadastro de notas (em desenvolvimento)

## 🛠️ Tecnologias utilizadas

- Python 3
- SQLite3 (banco de dados nativo do Python)
- Módulos padrão: `os`, `getpass`, `sqlite3`, `pathlib`

## 📂 Estrutura do Projeto

```
📦 sistema-usuarios
├── dbapi.py        # Arquivo com todas as funções de banco de dados
├── main.py         # Menu principal do sistema
├── banco_de_dados.db # Banco de dados SQLite (gerado automaticamente)
└── README.md
```

## ⚙️ Como executar

1. Clone este repositório ou copie os arquivos para uma pasta local:

   ```bash
   git clone https://github.com/seuusuario/sistema-usuarios.git
   cd sistema-usuarios
   ```

2. Execute o arquivo principal:

   ```bash
   python main.py
   ```

3. Use as opções do menu para **login** ou **cadastro**.

## 🔑 Usuário Padrão

Ao iniciar o sistema pela primeira vez, é criado automaticamente um administrador padrão:

```
Usuário: admin
Email:   admin@gmail
Senha:   admin
```

⚠️ **Recomenda-se trocar a senha após o primeiro acesso!**

## 📌 Próximos Passos

- Implementar criptografia de senha (`hashlib` ou `bcrypt`)
- Melhorar validações de entrada
- Criar testes automatizados
- Implementar cadastro de notas
- Futuramente: interface gráfica (Tkinter) ou web (Flask/Django)

---

👨‍💻 Desenvolvido por **[Allyson Gonçalves]**

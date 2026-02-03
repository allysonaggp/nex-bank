## 🏦 NexBank

**NexBank** é uma aplicação bancária digital desenvolvida com foco em escalabilidade, segurança e experiência do usuário. O projeto simula operações reais de um sistema financeiro, oferecendo funcionalidades como cadastro de clientes, autenticação segura, transferências entre contas, histórico de transações.

Construído com **Python** e utilizando **SQLAlchemy** como ORM, o NexBank integra-se a um banco de dados **PostgreSQL** para garantir robustez e confiabilidade na persistência dos dados. A interface web, desenvolvida em **HTML e CSS**, é totalmente **responsiva**, permitindo acesso fluido tanto em dispositivos móveis quanto em desktops.

Além disso, o sistema implementa práticas modernas de segurança, como o uso de **hashes criptográficos com `werkzeug.security`**, protegendo as credenciais dos usuários e reforçando a integridade da aplicação.

> Este projeto é ideal para fins educacionais, demonstrações técnicas ou como base para soluções bancárias mais complexas.


> 🚧 Projeto em desenvolvimento



## 🚀 Funcionalidades
- Cadastro e login de usuários com criptografia segura  
- Interface web responsiva (desktop e mobile)  
- Transferência entre contas  
- Histórico de transações  
- Painel administrativo com controle de usuários  
- Criação automática de administrador padrão

---

## 🛠 Tecnologias Utilizadas

| Camada         | Tecnologias                          |
|----------------|--------------------------------------|
| Backend        | Python, Flask, SQLAlchemy, PostgreSQL       |
| Segurança      | `werkzeug.security` (hash de senhas) |
| Frontend       | HTML, CSS ,JavaSxcript                            |
| Interface Web  | Flask (se estiver usando)            |

---

## 📱 Interface Responsiva

A interface foi projetada com foco em **usabilidade e acessibilidade**, adaptando-se a diferentes tamanhos de tela:

- Compatível com **desktops**, **notebooks**, **tablets** e **smartphones**
- Layout adaptativo com CSS moderno
- Navegação fluida e intuitiva

---

## 🔐 Segurança

- As senhas dos usuários são protegidas com **hashes gerados pelo `werkzeug.security`**, garantindo que nenhuma senha seja armazenada em texto plano.
- Recomenda-se alterar a senha do administrador padrão após o primeiro login.

---
## 🧑‍💻 Primeiro Administrador

O primeiro administrador é criado automaticamente com os seguintes dados:

* **Email:** admin\@nexbank.com
* **Senha:** admin

> ⚠️ Recomenda-se alterar a senha do administrador após o primeiro login.

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
python app.py
```

4. Use o menu para login, cadastro ou acessar funcionalidades de administrador.

---


✅ Tela de login

![alt text](/fotos/login.png)

✅ Tela de cadastro

![alt text](/fotos/cadastro.png)

✅ Tela de interface

![alt text](/fotos/home.png)

✅ Tela de Transferência

![alt text](/fotos/transferencia.png)

✅ Tela de interface responsiva

![alt text](/fotos/resposividade.png)

---






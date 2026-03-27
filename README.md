# Sistema Escolar — FastAPI

Sistema web para gerenciamento de alunos com autenticação por JWT.

## Tecnologias

- **FastAPI** — backend e rotas
- **SQLAlchemy** — ORM (SQLite local / PostgreSQL produção)
- **Jinja2** — templates HTML
- **Bootstrap 5** — interface
- **JWT (jose)** — autenticação via cookie httpOnly

## Estrutura

```
projeto/
├── main.py                    # Inicialização da aplicação
├── requirements.txt
├── .env.example               # Modelo de variáveis de ambiente
├── .gitignore
└── app/
    ├── core/
    │   ├── config.py          # Configurações (lê do .env)
    │   └── security.py        # Hash de senha e JWT
    ├── database/
    │   └── session.py         # Engine e sessão do banco
    ├── models/
    │   ├── aluno.py           # Model Aluno
    │   └── usuario.py         # Model Usuario
    ├── schemas/
    │   └── aluno.py           # Schemas Pydantic
    ├── services/
    │   └── aluno_service.py   # Lógica de negócio dos alunos
    ├── routes/
    │   ├── auth.py            # Login, registro, logout
    │   └── alunos.py          # CRUD de alunos (protegido)
    ├── templates/             # HTML Jinja2
    └── static/                # CSS, imagens, uploads
```

## Configuração

```bash
# 1. Clone e entre no diretório
cd projeto

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite .env com sua DATABASE_URL e SECRET_KEY

# 5. Inicie o servidor
uvicorn main:app --reload
```

Acesse em: http://localhost:8000

## Rotas disponíveis

| Método | Rota                        | Descrição                    |
|--------|-----------------------------|------------------------------|
| GET    | `/`                         | Página de login/registro     |
| POST   | `/login`                    | Autenticar                   |
| POST   | `/registrar`                | Criar conta                  |
| GET    | `/logout`                   | Encerrar sessão              |
| GET    | `/alunos/web`               | Listar alunos (protegido)    |
| GET    | `/alunos/dashboard`         | Dashboard (protegido)        |
| GET    | `/alunos/form`              | Formulário de cadastro       |
| POST   | `/alunos/web`               | Criar aluno                  |
| GET    | `/alunos/editar/id/{id}`    | Formulário de edição         |
| POST   | `/alunos/editar/id/{id}`    | Salvar edição                |
| POST   | `/alunos/deletar/id/{id}`   | Deletar aluno (via POST)     |

## Segurança

- Senhas armazenadas com bcrypt
- Autenticação via JWT em cookie `httpOnly`
- Cada usuário vê apenas seus próprios alunos
- Deleção via POST (protegida contra CSRF)
- Validação de tipo e tamanho de arquivo no upload
- Rotas de manutenção do banco removidas da aplicação

## Produção

Antes de ir para produção:
1. Gere uma `SECRET_KEY` forte: `python -c "import secrets; print(secrets.token_hex(32))"`
2. Configure `DATABASE_URL` para PostgreSQL
3. Defina `secure=True` no `set_cookie` (requer HTTPS)
4. Use um servidor como Gunicorn + Nginx

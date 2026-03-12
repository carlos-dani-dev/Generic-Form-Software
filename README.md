#### Esse é um repositório de documentação do processo de criação do **Generic Form Software**

#### O Generic Form Software é uma aplicação web para criação e preenchimento de formulários dinâmicos (pesquisas), com suporte a:

- autenticação com JWT;
- gerenciamento de pesquisas, perguntas e opções;
- perguntas dependentes (lógica condicional);
- registro de respostas por cidade;
- interface web com templates Jinja2.

#### Stack principal:

- Backend: FastAPI
- ORM: SQLAlchemy
- Banco de dados: PostgreSQL
- Templates: Jinja2
- Containerização: Docker + Docker Compose

#### Os componentes

- API FastAPI: disponibiliza endpoints REST e páginas renderizadas.
- PostgreSQL: persiste entidades de autenticação, pesquisas, perguntas e respostas.
- pgAdmin: interface web para administração do banco.

#### Resumo do funcionamento do software

1. Um usuário autenticado cria pesquisas e perguntas no painel administrativo.
2. O respondente escolhe a cidade e inicia uma resposta para uma pesquisa.
3. As perguntas são apresentadas, incluindo dependências entre questões.
4. As respostas são registradas em response, answer e answer_option.

#### Pré-requisitos para execução do projeto

- Docker e Docker Compose (recomendado)
- ou Python 3.11+ e acesso a um PostgreSQL

#### Configuração de ambiente

O projeto usa variáveis em .env na raiz.

Exemplo de variáveis necessárias:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha
DB_NAME=TaNaMesa
PG_DATA=/var/lib/postgresql/data/pgdata

PGADMIN4_EMAIL=admin@example.com
PGADMIN4_PASSWORD=senha

SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://postgres:senha@postgres:5432/TaNaMesa

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
```

#### Execução com Docker (recomendado)

#### Subir serviços

```bash
docker compose up --build
```

Serviços disponíveis:

- API: http://localhost:8000
- Health check: http://localhost:8000/healthy
- pgAdmin: http://localhost:5050

#### Inicialização do banco

Os scripts em db/init são executados automaticamente no primeiro start do PostgreSQL:

- 01_schema.sql: cria tabelas e relacionamentos
- 02_schema.sql: carga inicial (status, tipo de pergunta, cidades e usuário inicial)

## 6. Execução local (sem Docker)

### 6.1 Instalar dependências

```bash
pip install -r requirements.txt
```

#### Ajuste de SQLALCHEMY_DATABASE_URL no .env

Use um host local, por exemplo:

```env
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://postgres:senha@localhost:5432/TaNaMesa
```

#### Para rodar a aplicação

```bash
uvicorn App.main:app --host 0.0.0.0 --port 8000 --reload
```

#### A estrutura de diretórios

```text
App/
	main.py            # Inicialização da aplicação e registro dos routers
	config.py          # Carrega variáveis de ambiente
	database.py        # Engine, SessionLocal e Base do SQLAlchemy
	models.py          # Modelos ORM
	routers/           # Rotas da API e páginas
	templates/         # Páginas HTML (Jinja2)
	static/            # Arquivos estáticos (CSS e JS)

db/init/
	01_schema.sql      # Criação do schema
	02_schema.sql      # Seed inicial
```

#### Principais rotas

### 8.1 Saúde

- GET /healthy

#### Autenticação (/auth)

- GET /auth/login-page
- POST /auth/ (criação de usuário)
- POST /auth/token (login OAuth2 password flow)

#### Administração (/admin)

- GET /admin/survey
- GET /admin/question/{survey_id}
- GET /admin/create-survey
- GET /admin/create-question/{survey_id}
- GET /admin/dependency/{question_id}

#### Pesquisas (/survey)

- GET /survey/status
- POST /survey/status/create
- GET /survey
- POST /survey/create/{survey_status_id}
- GET /survey/city/{survey_id}
- GET /survey/fill/{survey_id}

#### Perguntas (/question)

- GET /question/{survey_id}
- POST /question/create/{survey_id}
- PUT /question/update/{question_id}
- GET /question/question-option/{question_id}
- POST /question/question_option/create/{question_id}
- POST /question/dependency/{question_id}/create
- GET /question/dependency/{question_id}/{question_option_id}/{survey_id}

#### Respostas e respostas-opção

- Response (/response): criação e consulta de respostas por pesquisa
- Answer (/answer): criação de respostas textuais e vínculos com opções

#### Cidades (/city)

- GET /city/{city_id}
- POST /city/create

#### Autenticação e sessão do software

- Login administrativo usa token JWT retornado em /auth/token.
- Rotas administrativas validam token de acesso em cookie access_token.
- Fluxo de preenchimento de pesquisa usa auth_token (cookie) para identificar response_id/survey_id da sessão de resposta.

#### O banco de dados definido para o projeto

Entidades principais:

- users
- survey_status
- survey
- question_type
- question
- question_option
- question_dependency
- response
- answer
- answer_option
- city

Relacionamentos importantes:

- Survey 1:N Question
- Question 1:N QuestionOption
- Response 1:N Answer
- Answer N:N QuestionOption (via AnswerOption)
- QuestionDependency conecta perguntas por opção de origem

#### Observações finais

- A aplicação exige SECRET_KEY no .env para inicializar o módulo de autenticação.
- O create_all() em startup cria tabelas mapeadas pelo SQLAlchemy (útil em desenvolvimento).
- O diretório de arquivos estáticos é montado em /static.

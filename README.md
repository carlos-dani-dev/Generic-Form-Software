# Software de questionário genérico

<p>Esta é uma aplicação web para criação e preenchimento de questionários dinâmicos (pesquisas de campo).<br>
Através deste software é possível tanto cadastrar e gerenciar respostas via login de administrador, como respondê-las de maneira anônima.</p>


### Features principais
- autenticação via JWT.
- gerenciamento de pesquisas completas, perguntas e alternativas.
- perguntas dependentes (lógica condicional).
- registro de respostas por cidade.
- interface web com templates Jinja2.
- alta disponibilidade via alocação em instância única de EC2 na AWS (ainda sem Load Balancer).

### Tecnologias utilizadas:

<table>
    <tr>
        <td>
            <strong>Ferramenta</strong>
        </td>
        <td>
            <strong>Descrição do uso</strong>
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://www.python.org/" target="_blank">Python</a>
        </td>
        <td>
            A linguagem base de todo o projeto.
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>
        </td>
        <td>
            Framework Python para desenvolvimento dos endpoints do backend de maneira assícrona por padrão.
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://www.sqlalchemy.org/">SQLAlchemy</a>
        </td>
        <td>Framework Python ideal para manipulação do banco de dados. O SQLAlchemy é a ORM mais utilizada em linguagem Python.</td>
    </tr>
    <tr>
        <td>
            <a href="https://www.postgresql.org/" target="_blank">PostgreSQL</a>
        </td>
        <td>
            Plataforma de banco de dados relacionais escolhida, pensando na importância de praticá-la em virtude da alta demanda do mercado atual.
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://jinja.palletsprojects.com/en/stable/" target="_blank">Jinja2</a>
        </td>
        <td>
            Framework Python de desenvolvimento frontend escolhida, pensando na praticidade de aplicação no contexto deste projeto.
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://docs.docker.com/compose/" target="_blank">Docker + Docker Compose</a>
        </td>
        <td>
            Ferramenta de containerização dos componentes utilizados. Facilita a execução de todos os serviços, além de simplifcar o deploy dentro da instância EC2 da AWS.
        </td>
    </tr>
</table>

### Os componentes da aplicação

- API FastAPI : Disponibiliza endpoints REST e páginas renderizadas. A saúde da API pode ser verificada em <a href="http://localhost:8000/healthy">http://localhost:8000/healthy</a>.
- PostgreSQL : Persiste entidades de autenticação, pesquisas, perguntas e respostas.
- pgAdmin : Interface web para administração do banco. Pode ser verificado em <a href="http://localhost:5050">http://localhost:5050</a>.

### Resumo do funcionamento do software

1. Um usuário autenticado cria pesquisas e perguntas no painel administrativo.
2. O respondente escolhe a cidade e inicia uma resposta para uma pesquisa.
3. As perguntas são apresentadas, incluindo dependências entre questões.
4. As respostas são registradas em response, answer e answer_option.

### Como rodar o projeto

##### Pré-requisitos para execução do projeto

<p>Para rodar a aplicação é necessário a instalação do Docker e do Docker Compose, além do Python 3.11+ com acesso a uma string de conexão a um banco de dados PostgreSQL</p>
<p>O projeto usa variáveis em .env na raiz.</p>

Exemplo do arquivo de variáveis de ambiente:

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

<p>Para subir o contâiner do docker, rode, via terminal, o seguinte comando:</p>

```bash
docker compose up --build
```

<p>Os scripts em db/init são executados automaticamente no primeiro start do PostgreSQL:</p>

- 01_schema.sql: cria tabelas e relacionamentos
- 02_schema.sql: carga inicial (status, tipo de pergunta, cidades e usuário inicial)

<p>As dependências necessárias são listadas em requirements.txt e podem ser instaladas automaticamente, via terminal, com o comando abaixo:</p>

```bash
pip install -r requirements.txt
```

### A estrutura de diretórios da aplicação

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

### As principais rotas da aplicação

<table>
	<tr>
		<td>
			Saúde	
		</td>
		<td>
			GET /healthy	
		</td>
	</tr>
	<tr>
		<td>
			Autenticação (/auth)
		</td>
		<td>
			GET /auth/login-page
			POST /auth/ (criação de usuário)
			POST /auth/token (login OAuth2 password flow)
		</td>
	</tr>
	<tr>
		<td>
			Administração (/admin)
		</td>
		<td>
			GET /admin/survey
			GET /admin/question/{survey_id}
			GET /admin/create-survey
			GET /admin/create-question/{survey_id}
			GET /admin/dependency/{question_id}			
		</td>
	</tr>
	<tr>
		<td>
			Pesquisas (/survey)
		</td>
		<td>
			GET /survey/status
			POST /survey/status/create
			GET /survey
			POST /survey/create/{survey_status_id}
			GET /survey/city/{survey_id}
			GET /survey/fill/{survey_id}
		</td>
	</tr>
	<tr>
		<td>
			Perguntas (/question)
		</td>
		<td>
			GET /question/{survey_id}
			POST /question/create/{survey_id}
			PUT /question/update/{question_id}
			GET /question/question-option/{question_id}
			POST /question/question_option/create/{question_id}
			POST /question/dependency/{question_id}/create
			GET /question/dependency/{question_id}/{question_option_id}/{survey_id}			
		</td>
	</tr>
	<tr>
		<td>
			Respostas e respostas-opção
		</td>
		<td>
			Response (/response): criação e consulta de respostas por pesquisa
			Answer (/answer): criação de respostas textuais e vínculos com opções			
		</td>
	</tr>
	<tr>
		<td>
			Cidades (/city)
		</td>
		<td>
			GET /city/{city_id}
			POST /city/create			
		</td>
	</tr>
</table>

### A autenticação de sessão do software

- Login administrativo usa token JWT retornado em /auth/token.
- Rotas administrativas validam token de acesso em cookie access_token.
- Fluxo de preenchimento de pesquisa usa auth_token (cookie) para identificar response_id/survey_id da sessão de resposta.

### O banco de dados definido para o projeto

<table>
	<tr>
		<td>Entidades principais</td>
	</tr>
	<tr>
		<td>
			users
			survey_status
			survey
			question_type
			question
			question_option
			question_dependency
			response
			answer
			answer_option
			city			
		</td>
	</tr>
</table>

<table>
	<tr>
		<td>Relacionamentos importantes</td>
	</tr>
	<tr>
		<td>
			Survey 1:N Question
			Question 1:N QuestionOption
			Response 1:N Answer
			Answer N:N QuestionOption (via AnswerOption)
			QuestionDependency conecta perguntas por opção de origem			
		</td>
	</tr>
</table>

### Observações finais

- A aplicação exige SECRET_KEY no .env para inicializar o módulo de autenticação.
- O create_all() em startup cria tabelas mapeadas pelo SQLAlchemy (útil em desenvolvimento).
- O diretório de arquivos estáticos é montado em /static.

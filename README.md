# Sistema de Contagem de Estoque

Este é um aplicativo web desenvolvido com Flask (backend) e HTML/CSS/JavaScript (frontend) para auxiliar na contagem e gestão de estoque, permitindo o cadastro de produtos, busca, resumo e geração de relatórios em PDF e Excel.

## Funcionalidades

- **Cadastro de Produtos:** Adicione produtos com código, nome, lote, data de validade e quantidade.
- **Busca e Contagem:** Pesquise produtos por código e visualize detalhes por lote.
- **Resumo do Estoque:** Obtenha um resumo consolidado do estoque, agrupado por código de produto, com quantidades totais e número de lotes.
- **Relatórios:** Gere relatórios detalhados em PDF e Excel, com informações por lote, subtotais por produto e total geral.
- **Limpar Dados:** Botão para apagar todos os dados do estoque e iniciar uma nova contagem do zero (com confirmação).

## Estrutura do Projeto

```
estoque-app/
├── src/
│   ├── main.py             # Ponto de entrada da aplicação Flask
│   ├── models/             # Modelos de banco de dados (Produto)
│   │   ├── __init__.py
│   │   └── produto.py
│   ├── routes/             # Rotas da API (produtos, relatórios)
│   │   ├── __init__.py
│   │   ├── produto.py
│   │   └── relatorio.py
│   └── static/             # Arquivos estáticos do frontend (HTML, CSS, JS)
│       └── index.html
├── venv/                   # Ambiente virtual Python
├── .flaskenv               # Variáveis de ambiente do Flask
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## Como Configurar e Rodar Localmente

Siga os passos abaixo para configurar e executar o aplicativo em seu ambiente local:

### 1. Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### 2. Clonar o Repositório (se aplicável)

Se você recebeu o código via um repositório Git, clone-o:

```bash
git clone <URL_DO_REPOSITORIO>
cd estoque-app
```

Se você recebeu o código como um arquivo ZIP, descompacte-o e navegue até o diretório `estoque-app`.

### 3. Criar e Ativar o Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto:

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows
```

### 4. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente

O Flask usa o arquivo `.flaskenv` para carregar variáveis de ambiente. Certifique-se de que ele existe e contém:

```
FLASK_APP=src/main.py
FLASK_ENV=development
```

### 6. Inicializar o Banco de Dados

O aplicativo usa SQLite, e o banco de dados será criado automaticamente na primeira execução se não existir. Para garantir que o esquema do banco de dados seja criado, você pode rodar o `main.py` uma vez ou simplesmente iniciar o servidor.

### 7. Rodar o Aplicativo

Com o ambiente virtual ativado, execute o servidor Flask:

```bash
flask run
```

O aplicativo estará acessível em `http://127.0.0.1:5000` (ou `http://localhost:5000`).

## Deploy em Plataformas Gratuitas (Ex: Render, Heroku, Railway)

Para um deploy permanente, você pode usar serviços de hospedagem que suportam aplicações Python/Flask. Abaixo, um guia geral para o Render.com, que oferece um plano gratuito generoso.

### Deploy no Render.com (Exemplo)

1. **Crie uma conta no Render:** Acesse [render.com](https://render.com/) e crie uma conta (você pode usar seu GitHub).

2. **Conecte seu Repositório Git:** Se seu código estiver no GitHub, GitLab ou Bitbucket, conecte-o ao Render. Se não, você pode fazer upload manual ou usar o Render CLI.

3. **Crie um Novo Serviço Web:**
   - No dashboard do Render, clique em `New` -> `Web Service`.
   - Selecione seu repositório (ou faça upload manual).
   - **Nome:** Dê um nome ao seu serviço (ex: `estoque-app`).
   - **Região:** Escolha a região mais próxima dos seus usuários.
   - **Branch:** `main` (ou a branch que contém seu código).
   - **Root Directory:** `/` (se seu `main.py` estiver na raiz do projeto, ou `src/` se o projeto for como a estrutura fornecida).
   - **Runtime:** `Python 3`.
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn src.main:app` (Para produção, `gunicorn` é mais robusto que `flask run`. Certifique-se de ter `gunicorn` no seu `requirements.txt`).
   - **Plano:** Escolha `Free`.

4. **Variáveis de Ambiente (Environment Variables):**
   - Adicione `FLASK_APP=src/main.py`
   - Adicione `FLASK_ENV=production` (para ambiente de produção)
   - Adicione `DATABASE_URL=sqlite:///instance/estoque.db` (ou a URL do seu banco de dados, se usar um externo como PostgreSQL).

5. **Deploy:** Clique em `Create Web Service`. O Render irá construir e implantar seu aplicativo. O processo pode levar alguns minutos na primeira vez.

6. **Acesse seu Aplicativo:** Após o deploy, o Render fornecerá uma URL pública para seu aplicativo.

### Considerações para Deploy

- **Banco de Dados:** Para o SQLite (`estoque.db`), o Render (e a maioria das plataformas gratuitas) usa um sistema de arquivos efêmero, o que significa que os dados serão perdidos a cada deploy ou reinício do serviço. Para persistência de dados em produção, é altamente recomendável usar um banco de dados externo (como PostgreSQL, que o Render também oferece um plano gratuito para bancos de dados).
- **Gunicorn:** Para produção, `gunicorn` é um servidor WSGI robusto. Certifique-se de adicioná-lo ao seu `requirements.txt` (`pip install gunicorn`).
- **Variáveis de Ambiente:** Sempre use variáveis de ambiente para configurações sensíveis ou que mudam entre ambientes (desenvolvimento/produção).

## Contato

Para dúvidas ou suporte, entre em contato com o desenvolvedor.


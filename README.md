# Passo a passo inicial

## Instalação

### 1 - pipx
Para instalar o pipx:

```
$ Execução no terminal

pip install --user pipx
```

Para o nosso sistema reconhecer o caminho das ferramentas instaladas via pipx podemos executar o comando:

```
$ Execução no terminal!

pipx ensurepath
```

### 2 - poetry
Para instalar o poetry:

```
$ Execução no terminal!

pipx install poetry
```

Para adicionar o shell ao poetry:

<b> Via pipx: </b>

```
$ Execução no terminal!

pipx inject poetry poetry-plugin-shell
```

<b> Via poetry self</b>

```
$ Execução no terminal!

poetry self add poetry-plugin-shell
```

Após isso rodar o seguinte comando, para que o poetry crie por padrão as venvs dentro da pasta do projeto:

```
poetry config virtualenvs.in-project true
```

### 3 - Python

Para instalar o python da versão que vamos utilizar (3.13):

```
poetry python install 3.13
```

Uma resposta similar a esta deve ser retornada ao executar o comando:

Resposta do comando `poetry python install`
```
Downloading and installing 3.13.2 (cpython) ... Done 
Testing 3.13.2 (cpython) ... Done
```

## Iniciando um projeto

### 1 - iniciar nosso projeto

```
poetry new --nome_do_projeto
cd nome_do_projeto
```

Ele criará uma estrutura de arquivos e pastas como essa:

```
.
├── nome_do_projeto
│  └── __init__.py
├── pyproject.toml
├── README.md
└── tests
   └── __init__.py
```

### 2 - Versão do poetry

Para usar a versão especifica e criar nosso ambiente de desenvolvimento:

```
poetry env use 3.13
```

### 3 - Configurar pyproject

Em conjunto com essa instrução, devemos também especificar no Poetry que usaremos exatamente a versão 3.13 em nosso projeto. Para isso, alteramos o arquivo de configuração pyproject.toml na raiz do projeto:

pyproject.toml

```
[project]
# ...
requires-python = ">=3.13,<4.0"
```

### 4 - instalando FastAPI

Com toda a base do nosso projeto pronta, podemos finalmente instalar o FastAPI:
```
poetry install 
poetry add 'fastapi[standard]'
```

### 5 - Instalando as ferramentas de desenvolvimento

As ferramentas escolhidas são:

<b> - taskipy: </b> ferramenta usada para criação de comandos. Como executar a aplicação, rodar os testes, etc.

<b> - pytest: </b> ferramenta para escrever e executar testes

<b> - ruff: </b> Uma ferramenta que tem duas funções no nosso código:
    
    Um analisador estático de código (um linter), para dizer se não estamos infringindo alguma boa prática de programação;
    
    Um formatador de código. Para seguirmos um estilo único de código. Vamos nos basear na PEP-8.
    
<b>  - typos: </b> ferramenta para pegar erros de grafia em inglês no código. Como um não nativo de inglês, as vezes acabo escrevendo alguns nomes incorretos. Talvez isso ajude você também.

Para instalar essas ferramentas que usaremos em desenvolvimento, podemos usar um grupo de dependências (--group dev no poetry) focado nelas, para não serem instaladas quando nossa aplicação estiver em produção:

```
poetry add --group dev pytest pytest-cov taskipy ruff typos
```

## Configurando as ferramentas de desenvolvimento

Após a instalação das ferramentas de desenvolvimento, precisamos definir as configurações de cada uma individualmente no arquivo pyproject.toml.

### Ruff

Na configuração global do Ruff queremos alterar somente duas coisas. O comprimento de linha para 79 caracteres (conforme sugerido na PEP-8) e, em seguida, informaremos que o diretório de migrações de banco de dados será ignorado na checagem e na formatação:

pyproject.toml

```
[tool.ruff]
line-length = 79
extend-exclude = ['migrations']
```

### Linter

Durante a análise estática do código, queremos buscar por coisas específicas. No Ruff, precisamos dizer exatamente o que ele deve analisar. Isso é feito por códigos. Usaremos estes:

* <b> I (Isort): </b> Checagem de ordenação de imports em ordem alfabética

* <b> F (Pyflakes): </b> Procura por alguns erros em relação a boas práticas de código

* <b> E (Erros pycodestyle): </b> Erros de estilo de código

* <b> W (Avisos pycodestyle): </b> Avisos de coisas não recomendadas no estilo de código

* <b> PL (Pylint): </b> Como o F, também procura por erros em relação a boas práticas de código

* <b> PT (flake8-pytest): </b> Checagem de boas práticas do Pytest

pyproject.toml

```
[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT']
```

### Formatter

A formatação do Ruff praticamente não precisa ser alterada. Pois ele vai seguir as boas práticas e usar a configuração global de 79 caracteres por linha. A única alteração que farei é o uso de aspas simples ' no lugar de aspas duplas ":

pyproject.toml

```
[tool.ruff.format]
preview = true
quote-style = 'single'
```

### pytest

O Pytest é uma framework de testes, que usaremos para escrever e executar nossos testes. O configuraremos para reconhecer o caminho base para execução dos testes na raiz do projeto .:

pyproject.toml

```
[tool.pytest.ini_options]
pythonpath = "."
addopts = '-p no:warnings'
```

### Typos

O typos vai nos ajudar com alguns errinhos que acabam acontecendo enquanto escrevemos código em inglês. Para ignorar o typos em determinados arquivos, poderiamos fazer algo parecido com isso:

pyproject.toml

```
[tool.typos.files]
extend-exclude = ["*.md"] 
```

### Taskipy

Alguns comandos que criaremos agora no início:

pyproject.toml

```
[tool.taskipy.tasks]
pre_lint = 'typos'
lint = 'ruff check'
pre_format = 'ruff check --fix'
format = 'ruff format'
run = 'fastapi dev fast_zero/app.py'
pre_test = 'task lint'
test = 'pytest -s -x --cov=fast_zero -vv'
post_test = 'coverage html'
```

Os comandos definidos fazem o seguinte:

* <b> pre_lint: </b> faz a busca por typos de inglês
* <b> lint: </b> faz a checagem de boas práticas do código python
* <b> pre_format: </b> faz algumas correções de boas práticas automaticamente
* <b> format: </b> executa a formatação do código em relação às convenções de estilo de código
* <b> run: </b> executa o servidor de desenvolvimento do FastAPI
* <b> pre_test: </b> executa a camada de lint antes de executar os testes
* <b> test:  </b>executa os testes com pytest de forma verbosa (-vv) e adiciona nosso código como base de cobertura
* <b> post_test: </b> gera um report de cobertura após os testes

Para executar um comando, é bem mais simples, precisando somente passar a palavra ```task <comando>```.

<b> Comandos com prefixo pre e pos </b>

Todos os comandos do taskipy que apresentam prefixos como pre_comando ou post_comando não precisam ser executados diretamente. Por exemplo, se executarmos o comando task test ele executará o comando pre_test e caso tudo ocorra bem, sem erros, ele executará o test, caso não aconteçam erros, o post_test será executado.

## Repositório

### Criando o .gitignore
Executar o comando:

```
pipx run ignr -p python > .gitignore
```

### Iniciando o repositório
```
git init .
gh repo create
```

# Informações Adicionais

### PrinterSchema
foi utilizado o tipo ```IPvAnyAddress``` importado do pydantic, para saber mais → <b> [IPvAnyAddress](https://mintlify.wiki/pydantic/pydantic/api/network-types#ipvanyaddress) </b>

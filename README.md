Desafio Orama
===============================

Uma API REST simples usando Falcon web framework

Premissas
===========

A API funciona com Python 3.7v+, PostgresSQL.
É necessario que você tenha essas ferramentas instaladas antes
de continuar.

```
apt-get update
apt-get install python3.7
sudo apt-get install build-essential python-pip3 libffi-dev python-dev python3-dev libpq-dev git
sudo apt-get install postgresql-10
```
Instalação
============

Faço do download do ZIP através do github ou utilize o comando:

```
git clone https://github.com/andersonpicollo/desafio-orama.git
```

Requirements
=====================

É altamente recomendado que você crie um Python [virtualenv](https://virtualenv.pypa.io/en/stable/)
antes de  instalar as dependências do projeto. As principais dependencias
são: Falcon 2.0.0, gunicorn 19.9.0, marshmallow 2.19.2,
psycopg2 2.8.2, SQLAlchemy 1.3.4  e Cerberus 1.3.1. Voce pode instalar
todas elas usando o pip.

```
pip install -r requirements.txt 
```

Banco de Dados
===================
Para configuração do POSTGRES da aplicação crie um usuario
com nome de "orama" e senha "orama".

O nome do banco de dados é "desafio-orama"

Caso queira alterar esses valores, edite o arquivo:
database/____init____.py e procura esta linha:

```
engine = get_engine('postgresql+psycopg2://orama:orama@localhost/desafio-orama')
```


Como Usar
==========

Inicie o servidor da aplicação.
```
gunicorn -b 127.0.0.1:8000 app.main:application
```


Requests / Responses
====================

- __Criar um cliente__

-- REQUEST
```
type = [POST]
path = "/clientes"
content-type = "application/json" 
body = { "nome":"Anderson Luis", "cpf": "123.456.789-10" "email": "anderson@uol.com.br" }
```
-- RESPONSE
```
body = {
    "code": 200,
    "message": "OK"
    }
```

- __Detalhes Cliente__

-- REQUEST
```
type = [GET]
path = "/clientes"
```

-- RESPONSE
```
    {
        "contas": [],
        "cpf": "103.934.933-56",
        "email": "joses@bol.com.br",
        "id": 2,
        "nome": "Jose da Silva"
    },
    {
        "contas": [],
        "cpf": "182.456.895-67",
        "email": "joao@gmail.com",
        "id": 5,
        "nome": "Joao"
    }
```

-- REQUEST
```
type = [GET]
path = "/clientes/{cliente_id}"
```

-- RESPONSE
```
    {
        "contas": [],
        "cpf": "182.456.895-67",
        "email": "joao@gmail.com",
        "id": 5,
        "nome": "Joao"
    }
```

- __Criar uma conta__

-- REQUEST
```
type = [POST]
path = "/contas"
content-type = "application/json" 
body = { "tipo":"Poupança", "numero": "35678-10" "cliente_id": 5 }
```
-- RESPONSE
```
body = {
    "code": 200,
    "message": "OK"
    }
```

- __Extrato Total Conta__

-- REQUEST
```
type = [GET]
path = "/contas/{conta_id}"
```

-- RESPONSE
```
   { 
    movs : [
        {
            "created": "2019-06-04",
            "tipo": "debito",
            "valor": 78.56
        },
        {
            "created": "2019-06-04",
            "tipo": "debito",
            "valor": 12.56
        }
    ],
    "numero": "38584-7",
    "saldo": 4784.69
    }
```

- __Operação Credito__

-- REQUEST
```
type = [POST]
path = "/movimentacao"
body = {"conta_id":1, "valor": 3000.50}
```

-- RESPONSE
```
body = {
    "code": 200,
    "message": "OK"
    }
```


- __Operação Debito__

-- REQUEST
```
type = [DELETE]
path = "/movimentacao"
body = {"conta_id":1, "valor": 3000.50}
```

-- RESPONSE
```
body = {
    "code": 200,
    "message": "OK"
    }
```

- __Extrato por filtro data__

-- REQUEST
```
type = [GET]
path = "/movimentacao/2019-06-02/2019-06-03"
body = {"conta_id":1, "valor": 3000.50}
```

-- RESPONSE
```
[
    {
        "created": "2019-06-02",
        "tipo": "credito",
        "valor": 100
    },
    {
        "created": "2019-06-02",
        "tipo": "credito",
        "valor": 20
    },
    {
        "created": "2019-06-02",
        "tipo": "debito",
        "valor": 320
    },
    
    {
        "created": "2019-06-03",
        "tipo": "credito",
        "valor": 765.03
    }
]
```

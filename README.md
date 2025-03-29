# API de Carteiras Digitais

Esta API gerencia carteiras digitais e transações financeiras entre usuários. Ela foi desenvolvida com Django e Django REST Framework, utilizando PostgreSQL como banco de dados.

## Requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Python 3.13+
- PostgreSQL
- Pip e Virtualenv (opcional, mas recomendado)

## Instalação e Configuração

### 1. Clone o repositório
```sh
git clone https://github.com/felipedaniel777/desafio_backend.git
cd desafio_backend
```

### 2. Criação do ambiente virtual (opcional, mas recomendado)
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

### 3. Instale as dependências
```sh
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary
```

### 4. Configuração do banco de dados
Edite o arquivo `settings.py` e configure o banco de dados PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'desafio_backend',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Execute as migrações
```sh
python manage.py migrate
```

### 6. Criação de superusuário (opcional)
```sh
python manage.py createsuperuser
```

### 7. Popular o banco de dados com dados de teste
```sh
python populate_db.py
```

### 8. Iniciar o servidor
```sh
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

## Testes com Curl

### 1. Criar usuário
```sh
curl -X POST http://127.0.0.1:8000/api/usuarios/ -H "Content-Type: application/json" -d '{
  "username": "testando",
  "password": "senha123",
  "email": "teste@email.com"
}'

```
### 2. Autenticação (Obter Token JWT)
```sh
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "testando", "password": "senha123"}'
```

### 3. Consultar saldo da carteira
```sh
curl -X GET http://127.0.0.1:8000/api/carteira/ -H "Authorization: Bearer SEU_TOKEN"
```

### 4. Adicionar saldo à carteira
```sh
curl -X POST http://127.0.0.1:8000/api/carteira/adicionar_saldo/ -H "Content-Type: application/json" -H "Authorization: Bearer SEU_TOKEN" -d '{
  "valor": 500.00
}'
```

### 5. Transferência entre carteiras
```sh
curl -X POST http://127.0.0.1:8000/api/transacoes/ -H "Content-Type: application/json" -H "Authorization: Bearer SEU_TOKEN" -d '{
  "destinatario": "id_do_destinatario",
  "valor": 200.00
}'


```

### 6. Listar transações
```sh
curl -X GET http://127.0.0.1:8000/api/transacoes/ -H "Authorization: Bearer SEU_TOKEN"
```


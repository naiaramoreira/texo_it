
# API de Pior Filme do Golden Raspberry Awards

Este projeto é uma API RESTful desenvolvida com FastAPI.

## Como Executar

### Pré-requisitos
- Docker
- Docker Compose

### Instruções

1. Clone o repositório para sua máquina local.
2. Navegue até o diretório do projeto.
3. Execute o comando para construir e iniciar o container:
   ```
   docker-compose up --build
   ```
   Este comando irá construir a imagem Docker da aplicação e iniciar o container.

## Endpoints

A aplicação suporta os seguintes endpoints:

- `POST /movies`: Adiciona um novo filme.
- `GET /movies`: Lista todos os filmes.
- `PUT /movies/{movie_id}`: Atualiza um filme existente pelo ID.
- `DELETE /movies/{movie_id}`: Remove um filme pelo ID.
- `GET /search_movies`: Pesquisa filmes pelo título ou ano.
- `GET /producers/intervals`: Retorna os produtores com o maior e o menor intervalo entre dois prêmios consecutivos, conforme a especificação.

### Exemplos de Uso

#### cURL

- Adicionar um novo filme:
  ```
  curl -X 'POST' \
    'http://localhost:8080/movies' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "year": 2020,
    "title": "Novo Filme",
    "studios": "Estúdio X",
    "producers": "Produtor Y",
    "winner": false
  }'
  ```

- Listar todos os filmes:
  ```
  curl -X 'GET' \
    'http://localhost:8080/movies' \
    -H 'accept: application/json'
  ```

- Para obter os produtores com o maior e o menor intervalo entre prêmios consecutivos:
  ```
  curl -X 'GET' \ 'http://localhost:8080/producers/intervals' \ -H 'accept: application/json'
  ```


## Healthcheck

Para verificar se a aplicação está rodando, você pode acessar o endpoint de healthcheck:

- `GET /healthcheck`

```
curl -X 'GET' 'http://localhost:8080/healthcheck' -H 'accept: application/json'
```

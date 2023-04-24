# Projeto FastAPI com PostgreSQL e Docker Compose

Este projeto é uma aplicação FastAPI que utiliza PostgreSQL como banco de dados e é executada em um ambiente de contêineres com Docker Compose. Ele inclui um serviço adicional, o pgAdmin, para facilitar a administração do banco de dados.

## Arquitetura

O projeto é composto por 4 serviços principais:

1. `postgres`: Serviço de banco de dados PostgreSQL.
2. `pgadmin`: Serviço de administração do PostgreSQL utilizando o pgAdmin.
3. `app`: Serviço da aplicação FastAPI.
4. `nginx`: Serviço proxy reverso utilizando Nginx.

Esses serviços são gerenciados através do arquivo `docker-compose.yml`.

## Como construir e instalar as dependências

Para construir e instalar as dependências do projeto, siga os passos abaixo:

### Pré-requisitos

- Instale o [Docker](https://www.docker.com/get-started) e o [Docker Compose](https://docs.docker.com/compose/install/) em seu computador.

### Passos

1. Clone o repositório do projeto:

```bash
git clone https://github.com/seu_usuario/seu_projeto.git
cd seu_projeto

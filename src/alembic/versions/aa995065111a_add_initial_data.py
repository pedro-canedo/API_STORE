"""Add initial data

Revision ID: aa995065111a
Revises: 
Create Date: 2023-04-16 14:12:40.102169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column

from src.app.crud.users import password_encode

# revision identifiers, used by Alembic.
revision = 'aa995065111a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Tabela users temporária para inserção de dados
    users = table(
        "users",
        column("id", sa.Integer),
        column("name", sa.String),
        column("email", sa.String),
        column("password_hash", sa.String),
    )

    # Tabela products temporária para inserção de dados
    products = table(
        "products",
        column("id", sa.Integer),
        column("name", sa.String),
        column("description", sa.String),
        column("price", sa.Float),
    )

    # Tabela categories temporária para inserção de dados
    categories = table(
        "categories",
        column("id", sa.Integer),
        column("name", sa.String),
    )

    # Tabela products_categories temporária para inserção de dados
    products_categories = table(
        "products_categories",
        column("product_id", sa.Integer),
        column("category_id", sa.Integer),
    )

    # Inserir dados na tabela users
    op.bulk_insert(
        users,
        [
            {"id": 1, "name": "Pedro", "email": "pedro@teste.com", "password_hash": password_encode('teste')},
        ],
    )

    # Inserir dados na tabela products
    op.bulk_insert(
        products,
        [
            {"id": 1, "name": "Produto 1", "description": "Descrição do Produto 1", "price": 10.0},
            {"id": 2, "name": "Produto 2", "description": "Descrição do Produto 2", "price": 20.0},
        ],
    )

    # Inserir dados na tabela categories
    op.bulk_insert(
        categories,
        [
            {"id": 1, "name": "Categoria 1"},
            {"id": 2, "name": "Categoria 2"},
        ],
    )

    # Inserir dados na tabela products_categories
    op.bulk_insert(
        products_categories,
        [
            {"product_id": 1, "category_id": 1},
            {"product_id": 2, "category_id": 2},
        ],
    )


def downgrade():
    pass

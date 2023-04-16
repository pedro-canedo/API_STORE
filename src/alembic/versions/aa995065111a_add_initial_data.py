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
    
    users = table(
        "users",
        column("id", sa.Integer),
        column("name", sa.String),
        column("email", sa.String),
        column("password_hash", sa.String),
        column("is_admin", sa.Boolean),
    )
    
    addresses = table(
        "addresses",
        column("id", sa.Integer),
        column("user_id", sa.Integer),
        column("description", sa.String),
        column("postal_code", sa.String),
        column("street", sa.String),
        column("complement", sa.String),
        column("neighborhood", sa.String),
        column("city", sa.String),
        column("state", sa.String),
    )

    products = table(
        "products",
        column("id", sa.Integer),
        column("name", sa.String),
        column("description", sa.String),
        column("price", sa.Float),
    )

    categories = table(
        "categories",
        column("id", sa.Integer),
        column("name", sa.String),
    )

    products_categories = table(
        "products_categories",
        column("product_id", sa.Integer),
        column("category_id", sa.Integer),
    )

    op.bulk_insert(
        users,
        [
            {"id": 1, "name": "Pedro", "email": "pedro@teste.com", "password_hash": password_encode('teste'), "is_admin": True},
        ],
    )
    
    op.bulk_insert(
        addresses,
        [
            {
                "id": 1,
                "user_id": 1,
                "description": "Casa",
                "postal_code": "12345-678",
                "street": "Rua Principal",
                "complement": "Ap. 101",
                "neighborhood": "Bairro Central",
                "city": "Cidade Exemplo",
                "state": "CE",
            },
        ],
    )

    op.bulk_insert(
        products,
        [
            {"id": 1, "name": "Produto 1", "description": "Descrição do Produto 1", "price": 10.0},
            {"id": 2, "name": "Produto 2", "description": "Descrição do Produto 2", "price": 20.0},
        ],
    )

    op.bulk_insert(
        categories,
        [
            {"id": 1, "name": "Categoria 1"},
            {"id": 2, "name": "Categoria 2"},
        ],
    )

    op.bulk_insert(
        products_categories,
        [
            {"product_id": 1, "category_id": 1},
            {"product_id": 2, "category_id": 2},
        ],
    )


def downgrade():
    op.execute("TRUNCATE order_items CASCADE")
    op.execute("TRUNCATE orders CASCADE")
    op.execute("TRUNCATE products_categories CASCADE")
    op.execute("TRUNCATE products CASCADE")
    op.execute("TRUNCATE categories CASCADE")
    op.execute("TRUNCATE addresses CASCADE")
    op.execute("TRUNCATE users CASCADE")

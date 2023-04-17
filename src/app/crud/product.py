from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.category import Category
from src.app.models import Product
from src.app.schemas.product import ProductCreate



def create_product(db: AsyncSession, product: ProductCreate):
    """
    Cria um novo produto no banco de dados com as informações fornecidas.

    Args:
        db (AsyncSession): A sessão do banco de dados.
        product (ProductCreate): As informações do produto a ser criado.

    Returns:
        Product: O objeto `Product` criado no banco de dados.

    Raises:
        N/A
    """
    db_product = Product(name=product.name, description=product.description, price=product.price)

    categories = db.query(Category).filter(Category.id.in_(product.categories)).all()

    db_product.categories.extend(categories)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: AsyncSession, product_id: int):
    """
    Retorna o produto com o ID fornecido.

    Args:
        db (AsyncSession): A sessão do banco de dados.
        product_id (int): O ID do produto a ser retornado.

    Returns:
        Product: O objeto `Product` com o ID fornecido, ou `None` se não existir.

    Raises:
        N/A
    """
    return db.query(Product).filter(Product.id == product_id).first()

def get_productes(db: AsyncSession):
    """
    Retorna todos os produtos existentes no banco de dados.

    Args:
        db (AsyncSession): A sessão do banco de dados.

    Returns:
        List[Product]: Uma lista contendo todos os objetos `Product` existentes no banco de dados.

    Raises:
        N/A
    """
    return db.query(Product).all()

def update_product(db: AsyncSession, product_id: int, updated_product: ProductCreate):
    """
    Atualiza as informações do produto com o ID fornecido.

    Args:
        db (AsyncSession): A sessão do banco de dados.
        product_id (int): O ID do produto a ser atualizado.
        updated_product (ProductCreate): As novas informações do produto.

    Returns:
        Product: O objeto `Product` atualizado, ou `None` se não existir.

    Raises:
        N/A
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db_product.name = updated_product.name
    db_product.description = updated_product.description
    db_product.price = updated_product.price
    db_product.categories = db.query(Category).filter(Category.id.in_(updated_product.category_ids)).all()
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: AsyncSession, product_id: int):
    """
    Deleta o produto com o ID fornecido.

    Args:
        db (AsyncSession): A sessão do banco de dados.
        product_id (int): O ID do produto a ser deletado.

    Returns:
        bool: `True` se o produto foi deletado com sucesso, `False` se não existir.

    Raises:
        N/A
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
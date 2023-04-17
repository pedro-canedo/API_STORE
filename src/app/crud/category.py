from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import Category
from src.app.schemas.category import CategoryCreate

def create_category(db: AsyncSession, category: CategoryCreate):
    """
    Cria uma nova categoria no banco de dados.

    Args:
        db (AsyncSession): instância da conexão do banco de dados.
        category (CategoryCreate): instância da categoria a ser criada.

    Returns:
        Category: a categoria criada.
    """
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    return db_category

def get_category(db: AsyncSession, category_id: int):
    """
    Retorna a categoria correspondente ao ID informado.

    Args:
        db (AsyncSession): instância da conexão do banco de dados.
        category_id (int): ID da categoria a ser retornada.

    Returns:
        Category: a categoria correspondente ao ID informado ou None se não encontrada.
    """
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: AsyncSession):
    """
    Retorna todas as categorias do banco de dados.

    Args:
        db (AsyncSession): instância da conexão do banco de dados.

    Returns:
        List[Category]: lista contendo todas as categorias do banco de dados.
    """
    return db.query(Category).all()

def update_category(db: AsyncSession, category_id: int, updated_category: CategoryCreate):
    """
    Atualiza uma categoria existente no banco de dados.

    Args:
        db (AsyncSession): instância da conexão do banco de dados.
        category_id (int): ID da categoria a ser atualizada.
        updated_category (CategoryCreate): instância da categoria com as informações atualizadas.

    Returns:
        Category: a categoria atualizada ou None se não encontrada.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db_category.name = updated_category.name
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: AsyncSession, category_id: int):
    """
    Exclui uma categoria do banco de dados.

    Args:
        db (AsyncSession): instância da conexão do banco de dados.
        category_id (int): ID da categoria a ser excluída.

    Returns:
        bool: True se a categoria foi excluída com sucesso, False caso contrário.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    db.delete(db_category)
    db.commit()
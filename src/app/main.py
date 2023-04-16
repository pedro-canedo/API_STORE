from fastapi import FastAPI
from src.app.routers import user_router, address_router, category_router, product_router, order_router, cep, category
from src.app.database.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(address_router, prefix="/addresses", tags=["addresses"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(cep.router, prefix="/cep", tags=["cep"])
app.include_router(category.router, prefix="/categories", tags=["categories"])

@app.get("/")
def read_root():
    return {"Status": "app is running"}

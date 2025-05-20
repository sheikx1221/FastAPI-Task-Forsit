import database
from fastapi import FastAPI, APIRouter
from api.routes import inventory, sales, product

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

api_router = APIRouter()
api_router.include_router(inventory.router)
api_router.include_router(sales.router)
api_router.include_router(product.router)

app.include_router(api_router)
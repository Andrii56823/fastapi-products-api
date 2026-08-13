from fastapi import FastAPI

import schemas
from pydantic import BaseModel, Field
from database import engine, Base
import models
from routers import products
from database import SessionLocal
from routers import categories
from routers import users

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException
import models
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import ProductNotFoundException

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.exception_handler(ProductNotFoundException)
def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Product with id {exc.product_id} not found"}
    )

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(users.router)
#products_db = []

@app.get("/")
async def read_root(): 
    return {"message": "Hello, world"}



#CATEGORY




    
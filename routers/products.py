from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal
from typing import List
import auth
from exceptions import ProductNotFoundException

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ProductOut)
def new_product(product: schemas.Product, db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user) ):
    db_product = models.Product(name=product.name, price=product.price, in_stock=product.in_stock, category_id=product.category_id, owner_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/all", response_model=List[schemas.ProductOut])
def get_all_products(skip: int = 0, limit: int = 10, sort_by: str = "id", order: str = "asc", search: str = None,  db: Session = Depends(get_db)):
    query = db.query(models.Product)

    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))

    column = getattr(models.Product, sort_by, models.Product.id)
    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    products = query.offset(skip).limit(limit).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category_name":p.category.name
        })
    return result

@router.get("/filter")
def filter_products(category_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    return query.all()


@router.delete("/{product_id}")
def del_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.owner_id == current_user.id).first()
    if db_product is None:
        raise ProductNotFoundException(product_id)
    db.delete(db_product)
    db.commit()
    return {"message": f"Product {product_id} deleted"}


@router.put("/{product_id}")
def update_product(product_id: int, product: schemas.Product, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.owner_id == current_user.id).first()
    if db_product is None:
        raise ProductNotFoundException(product_id)
    db_product.name = product.name
    db_product.price = product.price
    db_product.in_stock = product.in_stock
    db.commit()
    db.refresh(db_product)
    return db_product
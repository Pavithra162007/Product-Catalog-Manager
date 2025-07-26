from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Product).offset(skip).limit(limit).all()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Deleted successfully"}

@app.get("/search/", response_model=List[schemas.Product])
def search_products(q: str, db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    matches = [p for p in all_products if q.lower() in p.title.lower() or q.lower() in p.description.lower()]
    return matches

@app.get("/suggestions/{product_id}", response_model=List[schemas.Product])
def suggest_similar(product_id: int, db: Session = Depends(get_db)):
    current = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not current:
        raise HTTPException(status_code=404, detail="Product not found")
    all_products = db.query(models.Product).filter(models.Product.id != product_id).all()
    suggestions = [p for p in all_products if p.category == current.category]
    return suggestions[:3]

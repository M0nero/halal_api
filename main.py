from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from database import get_db
from models import Product, SubCategory
from schemas import ProductBase, SearchBase

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"], 
    allow_headers=["*"],
)

# To get all the products
@app.get("/products")
async def get_products(search: SearchBase = None, db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    if search:
        products = db.query(Product).filter(
            func.lower(Product.product_name).contains(search.keyword.lower())).limit(limit).offset(skip).all()
    else:
        products = db.query(Product).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(products), 'products': products}


# To get all the products filtered by subcategory
@app.get("/products/subcategory/{subcategory_id}")
async def get_products(subcategory_id: int, search: SearchBase = None, db: Session = Depends(get_db), limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    if search:
        products = db.query(Product).filter(Product.subcategory_id == subcategory_id) \
            .filter(func.lower(Product.product_name).contains(search.keyword.lower())).limit(limit).offset(skip).all()
    else:
        products = db.query(Product).filter(Product.subcategory_id == subcategory_id).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(products), 'products': products}


# To get the product by ID
@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# To create a product
@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductBase, db: Session = Depends(get_db)):
    new_product = Product(**payload.dict())
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error {e}")


# To update product with given ID
@app.patch("/products/{product_id}")
async def update_product(product_id: int, payload: ProductBase, db: Session = Depends(get_db)):
    product_query = db.query(Product).filter(Product.id == product_id)
    product = product_query.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No product with ID {product_id} in database')
    
    update_data = payload.dict(exclude_unset=True)
    product_query.filter(Product.id == product_id).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(product)
    return product


# To delete product with given ID
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_query = db.query(Product).filter(Product.id == product_id) 
    product = product_query.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No product with ID {product_id} in database')
    
    product_query.delete(synchronize_session=False)
    db.commit()


# to get subcategories by category_id
@app.get("/subcategory/{category_id}") 
async def get_subcategories(category_id: int, db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    subcategories = db.query(SubCategory).filter(SubCategory.category_id == category_id).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(subcategories), 'subcategories': subcategories}
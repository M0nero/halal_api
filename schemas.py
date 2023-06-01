from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int | None = None
    halal_status: int
    product_description: str
    product_img: str
    product_name: str
    subcategory_id: int
    cis: str | None = None

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    id: int | None = None
    img_url: str
    name: str
    parent_id: int

    class Config:
        orm_mode = True

class SearchBase(BaseModel):
    keyword: str
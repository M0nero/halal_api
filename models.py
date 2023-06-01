from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    halal_status = Column(Integer, ForeignKey('halal_status.id'))
    product_description = Column(Text)
    product_img = Column(String)
    product_name = Column(String(255))
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))
    cis = Column(String(255))


class HalalStatus(Base):
    __tablename__ = 'halal_status'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String)
    name = Column(String(255))

class SubCategory(Base):
    __tablename__ = 'subcategories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    img_url = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
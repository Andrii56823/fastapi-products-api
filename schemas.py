from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    in_stock: bool = True
    category_id: int

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    category_name: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)

class CategoryOut(BaseModel):
    id: int
    name:str

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=18, le=100)
    email: str 
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    age: int
    email: str

    class Config:
        from_attributes = True
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



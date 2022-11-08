from pydantic import BaseModel

class Item(BaseModel):
    name: str
    quant: int
    price: float
    sold: int
    desc: str
    file_upload: str

class User(BaseModel):
    name: str
    passw: str

class CartItem(BaseModel):
    item_id: int
    user_name: str

class CartItemUpdate(BaseModel):
    item_id: int
    user_name: str
    new_quant: int

class UserAddress(BaseModel):
    user_name: str
    add: str
    city: str
    phone: str

class PayData(BaseModel):
    user_name: str
    name: str
    lname1: str
    lname2: str
    ccnum: str
    ccv: str

class UserName(BaseModel):
    user_name: str

class Reference(BaseModel):
    reference: str
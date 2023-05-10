from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool


app = FastAPI()


@app.get('/')
def index():
    return {'message': "hello world!"}


@app.get('/greet/{name}')
def greet_name(name: str):
    return {'greeting': f'hello {name}'}

@app.get('/greet')
def greet_optional(name:Optional[str]="user"):
    return {"greeting":f"hello {name}"}

@app.put('/item/{item_id}')
def update_item(item_id: int, item: Item):
    return {"name": item.name,
            "description": item.description,
            "price": item.price,
            "on_offer": item.on_offer}

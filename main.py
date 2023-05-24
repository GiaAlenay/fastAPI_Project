from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker,relationship,joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey, Table
from pydantic import BaseModel
from typing import Optional,List

#cambiar con sus datos en este caso la base de datos la llame item_db
DATABASE_URL = "postgresql://postgres:postgres@localhost/item_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
association_table = Table(
    'user_item_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    users = relationship("User", secondary=association_table, back_populates="items")
    # back_populates='items' no es por el nombre de la tabla si no por la referencia que tiene en la tabla de user

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True,index=True)
    full_name=Column(String(255),nullable=False )
    gender=Column(String(255), nullable=False )
    items = relationship("Item", secondary=association_table, back_populates="users")

class ItemAttributes(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    users: Optional[List[int]] 

class UserAttributes(BaseModel):
    id: Optional[int]
    full_name: Optional[str]
    gender: Optional[str]
    items: Optional[List[int]] 

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users

@app.get("/users/items")
def read_users_items(db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload(User.items)).all()
    return {"users": [user.__dict__ for user in users]}


@app.get("/users/{user_id}")
def read_user(user_id :int, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/")
def create_user(user: UserAttributes, db:Session=Depends(get_db)):
    db_user=User(full_name=user.full_name, gender=user.gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}")
def update_user(user_id:int , user: UserAttributes, db:Session=Depends(get_db)):
    db_user= db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.full_name:
        db_user.full_name=user.full_name
    if user.gender:
        db_user.gender=user.gender
    if user.items:
       items = db.query(Item).filter(Item.id.in_(user.items)).all()
       if len(items) != len(user.items):
           raise HTTPException(status_code=404, detail="One or more items not found.")
       db_user.items = items
        
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id:int, db:Session=Depends(get_db)):
    user= db.query(User).filter(User.id== user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(user)
    db.commit()
    return user  



@app.get("/items")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/")
def create_item(item: ItemAttributes, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemAttributes, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.name:
        db_item.name = item.name
    if item.description:
        db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)): 
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()

    return db_item

#     @app.delete("/items/{item_id}")
# def delete_item(item_id: int, db: Session = Depends(get_db)): 
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if not db_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     db.delete(db_item)
#     db.commit()

#     return db_item
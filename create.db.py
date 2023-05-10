from database import Base,engine
from model import Item
print('creating database ...')
Base.metadata.create_all(engine)

#para poder crear los cambios se necesita ejecutar este archivo :python create.db.py
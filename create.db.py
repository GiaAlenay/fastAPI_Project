from main import Base,engine
#para poder crear las tablas dentro de la db se necesita ejecutar este archivo :python create.db.py por si solo

print('creating database ...')
Base.metadata.create_all(engine)

from fastapi import FastAPI
app=FastAPI()
@app.get('/')
def index():
    return{'message':"hello world!"}

@app.get('/greet/{name}')
def greet_name(name:str):
    return {'greeting':f'hello {name}'}
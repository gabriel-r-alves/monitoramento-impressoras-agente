from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/scan/')
def scan():
    # 1 - Validar dados
    # 2 - Realizar scan
    # 3 - Enviar os dados
    return {'message':'Acessou printers'}

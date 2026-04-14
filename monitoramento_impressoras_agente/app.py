from http import HTTPStatus

from fastapi import FastAPI
from monitoramento_impressoras_agente.schemas import PrinterSchema, ListPrintersSchema, RespScanSchema, ListRespScanSchema

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


@app.post('/scan/printers/', status_code=HTTPStatus.CREATED, response_model=RespScanSchema)
def scan_printer(printer: PrinterSchema):
    return printer


@app.post('/scan/list-printers/', status_code=HTTPStatus.CREATED, response_model=ListRespScanSchema)
def scan_printer(list_printers: ListPrintersSchema):
    return ListRespScanSchema


#@app.post('/printers/list')
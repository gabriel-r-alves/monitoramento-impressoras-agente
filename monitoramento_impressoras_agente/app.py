from http import HTTPStatus

from fastapi import FastAPI

from monitoramento_impressoras_agente.scan import async_collect_snmp
from monitoramento_impressoras_agente.schemas import (
    ListPrintersSchema,
    ListRespScanSchema,
    PrinterSchema,
    RespScanSchema,
)

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


'''
@app.get('/scan/printers/', status_code=HTTPStatus.OK, response_model=RespScanSchema)
async def scan():
    # simulação
    ip = '192.168.50.57'
    branch_id = 1
    network_id = 1
    snmp_data = await async_collect_snmp(ip=ip, branch_id=branch_id, network_id=network_id)
    
    return snmp_data
'''


@app.post('/scan/printers/', status_code=HTTPStatus.CREATED, response_model=RespScanSchema)
async def scan_printer(printer: PrinterSchema):
    snmp_data = await async_collect_snmp(ip=str(printer.ip), branch_id=printer.branch_id, network_id=printer.network_id)
    return snmp_data


@app.post('/scan/list-printers/', status_code=HTTPStatus.CREATED, response_model=ListRespScanSchema)
def scan_list_printers(list_printers: ListPrintersSchema):
    # em desenvolvimento
    return ListRespScanSchema


if __name__ == "__main__":
    import asyncio
    import json

    ip = '192.168.50.57'
    branch_id = 1
    network_id = 1

    try:
        snmp_data = asyncio.run(async_collect_snmp(ip=ip, branch_id=branch_id, network_id=network_id))
        print(json.dumps(snmp_data))
    except Exception as e:
        print(f"Erro ao executar o teste: {e}")

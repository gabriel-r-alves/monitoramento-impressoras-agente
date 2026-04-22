from http import HTTPStatus

from fastapi import FastAPI

from monitoramento_impressoras_agente.scan import ScanService

from monitoramento_impressoras_core.schemas import (
    ListPrintersSchema,
    ListRespScanSchema,
    PrinterSchema,
    RespScanSchema,
)

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/scan/printers/', status_code=HTTPStatus.CREATED, response_model=RespScanSchema)
async def scan_printer(printer: PrinterSchema):
    scan_service = ScanService()
    snmp_data = await scan_service.async_collect_snmp(
        ip=str(printer.ip),
        branch_id=printer.branch_id,
        network_id=printer.network_id)
    
    return snmp_data


@app.post('/scan/list-printers/', status_code=HTTPStatus.CREATED, response_model=ListRespScanSchema)
async def scan_list_printers(list_printers: ListPrintersSchema):
    list_snmp_data = []
    scan_service = ScanService()

    for printer in list_printers:    
        snmp_data = await scan_service.async_collect_snmp(
            ip=str(printer.ip),
            branch_id=printer.branch_id,
            network_id=printer.network_id)
        
        list_snmp_data.append(snmp_data)

    return ListRespScanSchema


if __name__ == "__main__":
    import asyncio
    import json

    ip = '192.168.50.57' # ip de teste
    branch_id = 1
    network_id = 1

    try:
        scan_service = ScanService()
        snmp_data = asyncio.run(scan_service.async_collect_snmp(ip=ip, branch_id=branch_id, network_id=network_id))
        print(json.dumps(snmp_data))
    except Exception as e:
        print(f"Erro ao executar o teste: {e}")

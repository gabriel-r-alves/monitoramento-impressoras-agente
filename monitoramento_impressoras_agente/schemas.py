'''
Não utilizar este arquivo somente para testes, será removido!.

Os schemas estão from monitoramento_impressoras_core.schemas, é um repositorio git que serve como biblioteca, onde é compartilhado os schemas entre agente e backend.
'''

from pydantic import BaseModel, IPvAnyAddress


class Message(BaseModel):
    message: str


class PrinterSchema(BaseModel):
    ip: IPvAnyAddress
    network_id: int | None
    branch_id: int


class ListPrintersSchema(BaseModel):
    printers: list[PrinterSchema]


class SnmpResultSchema(BaseModel):
    num_serial: str
    model: str
    counter: str


class RespScanSchema(BaseModel):
    connection: str | None
    ip: IPvAnyAddress
    network_id: int
    branch_id: int
    result: SnmpResultSchema | dict


class ListRespScanSchema(BaseModel):
    list_resps: list[RespScanSchema]

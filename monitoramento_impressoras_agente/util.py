import aioping

from pysnmp.hlapi.asyncio import *
from pysnmp.entity.engine import SnmpEngine

from .loggin import log_info, log_error

async def scan(ip):
    try:
        delay = await aioping.ping(ip, timeout=3)
        return True
    except TimeoutError:
        return False
    except Exception as e:
        # Adicione este print temporário para ver o erro real no console
        print(f"ERRO NO PING para {ip}: {e}") 
        return False

async def snmp(ip, listaSnmp=''):
    community = 'public'  # Comunidade SNMP configurada na impressora

    oids = listaSnmp if listaSnmp else [
        '1.3.6.1.2.1.1.5.0',
        'iso.3.6.1.2.1.43.5.1.1.17.1',
        'iso.3.6.1.2.1.25.3.2.1.3.1',
        'iso.3.6.1.2.1.43.10.2.1.4.1.1'
    ]

    log_info(f"Iniciando consulta SNMP assíncrona para IP {ip}")

    try:
        error_indication, error_status, error_index, var_binds = await getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((ip, 161), timeout=3, retries=1),
            ContextData(),
            *[ObjectType(ObjectIdentity(oid)) for oid in oids]
        )
    except Exception as e:
        log_error(f"Erro crítico na conexão SNMP com {ip}: {e}")
        return []

    if error_indication:
        log_error(f"Erro SNMP em {ip}: {error_indication}")
        return []
    elif error_status:
        log_error(f"Erro na resposta SNMP em {ip}: {error_status.prettyPrint()}")
        return []

    results = []
    for oid, val in var_binds:
        results.append({'oid': str(oid), 'resposta': str(val)})
        #log_info(f"OID {oid} → Resposta: {val}")

    return results

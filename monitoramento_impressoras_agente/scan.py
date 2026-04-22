import aioping

from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.asyncio import *

from typing import Any

from monitoramento_impressoras_agente.logging_utils import log_error, log_info

SnmpResult = dict[str, Any]

class ScanService:
    def __init__(self):
        self.OID_MAP = {
            "1.3.6.1.2.1.43.5.1.1.17.1": "num_serial",
            "1.3.6.1.2.1.25.3.2.1.3.1": "model",
            "1.3.6.1.2.1.43.10.2.1.4.1.1": "counter"
        }

    async def async_collect_snmp(self, ip: str, branch_id: int, network_id: int | None) -> SnmpResult:
            log_info(f"Iniciando coleta SNMP no IP {ip}")

            snmp_data = {
                "connection": None,
                "ip": ip,
                "network_id": network_id,
                "branch_id": branch_id,
                "result": {}
            }

            log_info("Pingando IP...")
            is_online = await self.async_scan(ip)

            if not is_online:
                snmp_data["connection"] = "offline"
                log_error(f"[X] IP {ip} OFFLINE")
                return snmp_data

            snmp_data["connection"] = "online"
            log_info(f"[✓] IP {ip} online")

            try:
                oids = await self.async_snmp(ip)
                if not oids:
                    snmp_data["connection"] = "erro snmp"
                    log_error(f"[X] Erro ao obter dados SNMP no IP{ip}")
                    return snmp_data

                for oid in oids:
                    field = self.OID_MAP.get(oid["oid"])
                    if field:
                        snmp_data["result"][field] = oid["resposta"] or None

                if snmp_data['result'].get('num_serial') is None:
                    snmp_data["connection"] = "erro snmp"

            except Exception as e:
                log_error(f"Erro inesperado no SNMP do IP {ip}: {e}")
                snmp_data["connection"] = "erro snmp"
                return snmp_data

            log_info(f"Finalizando coleta SNMP no IP {ip}")
            return snmp_data


    @staticmethod
    async def async_scan(ip):
        try:
            delay = await aioping.ping(ip, timeout=3)
            return True
        except TimeoutError:
            return False
        except Exception as e:
            print(f"ERRO NO PING para {ip}: {e}")
            return False


    @staticmethod
    async def async_snmp(ip, listaSnmp=''):
        community = 'public'  # Comunidade SNMP

        oids = listaSnmp if listaSnmp else [
            '1.3.6.1.2.1.1.5.0',
            '1.3.6.1.2.1.43.5.1.1.17.1',
            '1.3.6.1.2.1.25.3.2.1.3.1',
            '1.3.6.1.2.1.43.10.2.1.4.1.1'
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

        return results

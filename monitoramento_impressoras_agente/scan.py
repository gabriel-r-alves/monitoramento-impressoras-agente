
from monitoramento_impressoras_agente.logging_utils import log_error, log_info

from .util import async_scan, async_snmp

OID_MAP = {
    "1.3.6.1.2.1.43.5.1.1.17.1": "num_serial",
    "1.3.6.1.2.1.25.3.2.1.3.1": "model",
    "1.3.6.1.2.1.43.10.2.1.4.1.1": "counter"
}

SnmpResult = dict[str, any]


async def async_collect_snmp(ip: str, branch_id: int, network_id: int | None) -> SnmpResult:
        log_info(f"Iniciando coleta SNMP no IP {ip}")

        snmp_data = {
            "connection": None,
            "ip": ip,
            "network_id": network_id,
            "branch_id": branch_id,
            "result": {}
        }

        log_info("Pingando IP...")
        is_online = await async_scan(ip)

        if not is_online:
            snmp_data["connection"] = "offline"
            log_error(f"[X] IP {ip} OFFLINE")
            return snmp_data

        snmp_data["connection"] = "online"
        log_info(f"[✓] IP {ip} online")

        try:
            oids = await async_snmp(ip)
            if not oids:
                snmp_data["connection"] = "erro snmp"
                log_error(f"[X] Erro ao obter dados SNMP no IP{ip}")
                return snmp_data

            for oid in oids:
                field = OID_MAP.get(oid["oid"])
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

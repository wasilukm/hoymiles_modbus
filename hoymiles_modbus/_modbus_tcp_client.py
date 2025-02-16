from dataclasses import asdict
from typing import TYPE_CHECKING

from pymodbus.client import ModbusTcpClient

if TYPE_CHECKING:  # pragma: no cover
    from .datatypes import CommunicationParams

SIZE_BYTE_POSITION = 8


def _data_size_fixer(sending: bool, data: bytes) -> bytes:
    if not sending:
        fixed_packet = list(data)
        fixed_packet[SIZE_BYTE_POSITION] = len(fixed_packet[SIZE_BYTE_POSITION + 1 :])  # calculate new data size
        return bytes(fixed_packet)
    return data


def create_modbus_tcp_client(host: str, port: int, comm_params: 'CommunicationParams') -> ModbusTcpClient:
    """Create an instance of Modbus TCP client.

    Arguments:
        host: Host IP address or host name
        port: port number
        comm_params: communication parameters

    """
    client = ModbusTcpClient(
        host=host,
        port=port,
        trace_packet=_data_size_fixer,
        **asdict(comm_params),
    )

    return client

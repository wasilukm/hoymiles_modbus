from dataclasses import asdict, dataclass

from pymodbus.client import ModbusTcpClient
from pymodbus.pdu.register_read_message import ReadHoldingRegistersResponse


@dataclass
class CommunicationParams:
    """Low level pymodbus communication parameters."""

    timeout: float = 3
    """Timeout for a connection request, in seconds."""
    retries: int = 3
    """Max number of retries per request."""
    reconnect_delay: float = 0
    """Minimum delay in seconds.milliseconds before reconnecting.
    Doubles automatically with each unsuccessful connect, from
    **reconnect_delay** to **reconnect_delay_max**.

    Default is 0 which means that reconnecting is disabled."""
    reconnect_delay_max: float = 300
    """Maximum delay in seconds.milliseconds before reconnecting."""


class _CustomReadHoldingRegistersResponse(ReadHoldingRegistersResponse):

    @staticmethod
    def _data_size_fixer(packet):
        fixed_packet = list(packet)
        if packet:
            fixed_packet[0] = len(fixed_packet[1:])  # calculate new data size
        return bytes(fixed_packet)

    def decode(self, data):
        fixed = self._data_size_fixer(data)
        return super().decode(fixed)


def create_modbus_tcp_client(host: str, port: int, comm_params: CommunicationParams) -> ModbusTcpClient:
    """Create an instance of Modbus TCP client.

    Arguments:
        host: Host IP address or host name
        port: port number
        comm_params: communication parameters

    """
    client = ModbusTcpClient(
        host=host,
        port=port,
        **asdict(comm_params),
    )

    # Register custom PDU class which fixed data size in response from DTU
    # (some DTUs send corrupted packets)
    client.framer.decoder.register(_CustomReadHoldingRegistersResponse)

    return client

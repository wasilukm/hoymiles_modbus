"""Hoymiles Modbus client."""

from dataclasses import asdict, dataclass
from typing import List, Type, Union

from pymodbus.client import ModbusTcpClient
from pymodbus.framer.old_framer_socket import ModbusSocketFramer

from .datatypes import (
    HMSeriesMicroinverterData,
    MicroinverterType,
    MISeriesMicroinverterData,
    PlantData,
    _serial_number_t,
)


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


class _CustomSocketFramer(ModbusSocketFramer):
    """Custom framer for fixing data length in received modbus packets."""

    @staticmethod
    def _data_length_fixer(packet):  # pragma: no cover
        fixed_packet = list(packet)
        if len(packet) > 9:
            fixed_packet[8] = len(fixed_packet[9:])
        return bytes(fixed_packet)

    def processIncomingPacket(self, data, callback, unit, **kwargs):
        fixed_data = self._data_length_fixer(data)
        super().processIncomingPacket(fixed_data, callback, unit, **kwargs)


class HoymilesModbusTCP:
    """Hoymiles Modbus TCP client.

    Gather data from photovoltaic installation based on Hoymiles microinverters managed by Hoymiles DTU (like DTU-pro).
    The client communicates with DTU via Modbus TCP protocol.

    """

    _MAX_MICROINVERTER_COUNT = 100
    _NULL_MICROINVERTER = '000000000000'

    def __init__(
        self, host: str, port: int = 502, microinverter_type: MicroinverterType = MicroinverterType.MI, unit_id: int = 1
    ) -> None:
        """Initialize the object.

        Arguments:
            host: DTU address
            port: target DTU modbus TCP port
            microinverter_type: Microinverter type, applies to all microinverters
            unit_id: Modbus unit ID

        """
        self._host: str = host
        self._port: int = port
        self._dtu_serial_number: str = ''
        self._microinverter_data_struct: Type[Union[MISeriesMicroinverterData, HMSeriesMicroinverterData]]
        if microinverter_type == MicroinverterType.MI:
            self._microinverter_data_struct = MISeriesMicroinverterData
        elif microinverter_type == MicroinverterType.HM:
            self._microinverter_data_struct = HMSeriesMicroinverterData
        else:
            raise ValueError('Unsupported microinverter type:', microinverter_type)
        self._unit_id = unit_id
        self._comm_params: CommunicationParams = CommunicationParams()

    @property
    def comm_params(self) -> CommunicationParams:
        """Low level communication parameters."""
        return self._comm_params

    def _get_client(self) -> ModbusTcpClient:
        client = ModbusTcpClient(
            host=self._host,
            port=self._port,
            **asdict(self.comm_params),
        )

        # reinitialize framer with custom framer, use already existing decoder
        # custom framer is for fixing data length in received frames
        # (some DTUs send corrupted packets)
        client.framer = _CustomSocketFramer(client.framer.decoder, client)
        return client

    @staticmethod
    def _read_registers(client: ModbusTcpClient, start_address, count, unit_id):
        result = client.read_holding_registers(start_address, count, slave=unit_id)
        if result.isError():
            raise RuntimeError(f'Received error response {result}')
        return result

    @property
    def microinverter_data(self) -> List[Union[MISeriesMicroinverterData, HMSeriesMicroinverterData]]:
        """Status data from all microinverters.

        Each `get` is a new request and data from the installation.

        """
        data: List[Union[MISeriesMicroinverterData, HMSeriesMicroinverterData]] = []
        with self._get_client() as client:
            for i in range(self._MAX_MICROINVERTER_COUNT):
                start_address = i * 40 + 0x1000
                result = self._read_registers(client, start_address, 20, self._unit_id)
                data_to_unpack = result.encode()[1:41]
                if i < 1 and len(data_to_unpack) < 1:
                    raise RuntimeError("Microinverters not mapped yet.")
                microinverter_data = self._microinverter_data_struct.unpack(data_to_unpack)
                if microinverter_data.serial_number == self._NULL_MICROINVERTER:
                    break
                data.append(microinverter_data)
        return data

    @property
    def dtu(self) -> str:
        """DTU serial number."""
        if not self._dtu_serial_number:
            with self._get_client() as client:
                result = self._read_registers(client, 0x2000, 3, self._unit_id)
                self._dtu_serial_number = _serial_number_t.unpack(result.encode()[1::])
        return self._dtu_serial_number

    @property
    def plant_data(self) -> PlantData:
        """Plant status data.

        Each `get` is a new request and data from the installation.

        """
        microinverter_data = self.microinverter_data
        data = PlantData(self.dtu, microinverter_data=microinverter_data)
        for microinverter in microinverter_data:
            if microinverter.link_status:
                data.pv_power += microinverter.pv_power
                data.today_production += microinverter.today_production
                data.total_production += microinverter.total_production
                if microinverter.alarm_code:
                    data.alarm_flag = True
        return data

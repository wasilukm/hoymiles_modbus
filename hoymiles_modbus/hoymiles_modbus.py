"""Main module."""

from typing import List

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.framer.socket_framer import ModbusSocketFramer

from ._datatype import MicroinverterData, PlantData, serial_number_t


class _CustomSocketFramer(ModbusSocketFramer):
    """Custom framer for fixing data length in received modbus packets."""

    @staticmethod
    def _data_length_fixer(packet):
        fixed_packet = list(packet)
        fixed_packet[8] = len(fixed_packet[9:])
        return bytes(fixed_packet)

    def processIncomingPacket(self, data, callback, unit, **kwargs):
        fixed_data = self._data_length_fixer(data)
        return super().processIncomingPacket(fixed_data, callback, unit, **kwargs)


class HoymilesModbusTCP:
    """Gather data through Modbus TCP.

    :param host: DTU address
    :param port: target DTU modbus TCP port

    """

    _MAX_MICROINVERTER_COUNT = 100
    _NULL_MICROINVERTER = b'000000000000'

    def __init__(self, host: str, port: int = 502) -> None:
        """Gather data through Modbus TCP."""
        self._host: str = host
        self._port: int = port
        self._dtu_serial_number: bytes = b''

    def _get_client(self):
        return ModbusTcpClient(self._host, self._port, framer=_CustomSocketFramer)

    @property
    def microinverter_data(self) -> List[MicroinverterData]:
        """Microinvertes status data."""
        data: List[MicroinverterData] = []
        with self._get_client() as client:
            for i in range(self._MAX_MICROINVERTER_COUNT):
                start_address = i * 40 + 0x1000
                result = client.read_holding_registers(start_address, 20, unit=1)
                microinverter_data = MicroinverterData.unpack(result.encode()[1:41])
                if microinverter_data.serial_number == self._NULL_MICROINVERTER:
                    break
                data.append(microinverter_data)
        return data

    @property
    def dtu(self) -> bytes:
        """DTU serial number."""
        if not self._dtu_serial_number:
            with self._get_client() as client:
                result = client.read_holding_registers(0x2000, 3, unit=1)
                self._dtu_serial_number = serial_number_t.unpack(result.encode()[1::])
        return self._dtu_serial_number

    @property
    def plant_data(self):
        """Plant status data."""
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

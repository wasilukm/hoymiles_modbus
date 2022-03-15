"""Hoymiles Modbus client."""

from typing import List, Type, Union

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.framer.socket_framer import ModbusSocketFramer

from .datatypes import (
    HMSeriesMicroinverterData,
    MicroinverterType,
    MISeriesMicroinverterData,
    PlantData,
    _serial_number_t,
)


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
    """Hoymiles Modbus TCP client.

    Gather data from photovoltaic installation based on Hoymiles microinverters managed by Hoymiles DTU (like DTU-pro).
    The client communicates with DTU via Modbus TCP protocol.

    """

    _MAX_MICROINVERTER_COUNT = 100
    _NULL_MICROINVERTER = '000000000000'

    def __init__(
        self, host: str, port: int = 502, microinverter_type: MicroinverterType = MicroinverterType.MI
    ) -> None:
        """Initialize the object.

        Arguments:
            host: DTU address
            port: target DTU modbus TCP port
            microinverter_type: Microinverter type, applies to all microinverters

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

    def _get_client(self) -> ModbusTcpClient:
        return ModbusTcpClient(self._host, self._port, framer=_CustomSocketFramer)

    @staticmethod
    def _read_registers(client: ModbusTcpClient, start_address, count):
        result = client.read_holding_registers(start_address, count, unit=1)
        if result.isError():
            raise result
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
                result = self._read_registers(client, start_address, 20)
                microinverter_data = self._microinverter_data_struct.unpack(result.encode()[1:41])
                if microinverter_data.serial_number == self._NULL_MICROINVERTER:
                    break
                data.append(microinverter_data)
        return data

    @property
    def dtu(self) -> str:
        """DTU serial number."""
        if not self._dtu_serial_number:
            with self._get_client() as client:
                result = self._read_registers(client, 0x2000, 3)
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

from binascii import hexlify
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional, Tuple, Union

from plum.array import ArrayX
from plum.bigendian import uint8, uint16, uint32
from plum.bytes import BytesX
from plum.decimal import DecimalX
from plum.dump import Record
from plum.structure import Structure, member


class SerialNumberX(BytesX):
    """Datatype for decoding serial number."""

    def __unpack__(
        self,
        buffer: bytes,
        offset: int,
        dump: Optional[Record] = None,
        nbytes: Optional[int] = None,
    ) -> Tuple[bytes, int]:
        """Unpack."""
        data, offset = super().__unpack__(buffer, offset, dump, nbytes)
        return hexlify(data), offset

    def __pack__(
        self,
        value: Union[bytes, bytearray],
        pieces: List[bytes],
        dump: Optional[Record] = None,
    ) -> None:
        """Pack."""
        raise NotImplementedError


udec16p1 = DecimalX('udec16p1', nbytes=2, precision=1, byteorder='big', signed=False)
sdec16p1 = DecimalX('sdec16p1', nbytes=2, precision=1, byteorder='big', signed=True)
udec16p2 = DecimalX('udec16p2', nbytes=2, precision=2, byteorder='big', signed=False)

serial_number_t = SerialNumberX('serial_number_t', nbytes=6)
reserved = ArrayX('reserved', fmt=uint8)


class MicroinverterData(Structure):
    """Microinverter status data."""

    data_type: int = member(fmt=uint8)
    serial_number: bytes = member(fmt=serial_number_t)
    port_number: int = member(fmt=uint8)
    pv_voltage: Decimal = member(fmt=udec16p1, doc='V')
    pv_current: Decimal = member(fmt=udec16p1, doc='A')
    grid_voltage: Decimal = member(fmt=udec16p1, doc='V')
    grid_frequency: Decimal = member(fmt=udec16p2, doc='Hz')
    pv_power: Decimal = member(fmt=udec16p1, doc='W')
    today_production: int = member(fmt=uint16, doc='Wh')
    total_production: int = member(fmt=uint32, doc='Wh')
    temperature: Decimal = member(fmt=sdec16p1, doc='°C')
    operating_status: int = member(fmt=uint16)
    alarm_code: int = member(fmt=uint16)
    alarm_count: int = member(fmt=uint16)
    link_status: int = member(fmt=uint8)
    reserved: List[int] = member(fmt=reserved)


@dataclass
class PlantData:
    """Data for the whole plant."""

    dtu: bytes
    """DTU serial number."""
    pv_power: Decimal = Decimal(0)
    """Current production."""
    today_production: int = 0
    """Today prodution."""
    total_production: int = 0
    """Total production."""
    alarm_flag: bool = False
    """Alarm indicator. True means that at least one microinverter reported an alarm."""
    microinverter_data: List[MicroinverterData] = field(default_factory=list)
    """Data for each microinverter."""

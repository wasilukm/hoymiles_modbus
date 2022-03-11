"""Data structures."""

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


class _SerialNumberX(BytesX):
    """Datatype for decoding serial number."""

    def __unpack__(  # type: ignore[override]
        self,
        buffer: bytes,
        offset: int,
        dump: Optional[Record] = None,
        nbytes: Optional[int] = None,
    ) -> Tuple[str, int]:
        """Unpack."""
        data, offset = super().__unpack__(buffer, offset, dump, nbytes)
        serial_bytes = hexlify(data)
        return serial_bytes.decode('ascii'), offset

    def __pack__(
        self,
        value: Union[bytes, bytearray],
        pieces: List[bytes],
        dump: Optional[Record] = None,
    ) -> None:
        """Pack."""
        raise NotImplementedError


_udec16p1 = DecimalX('udec16p1', nbytes=2, precision=1, byteorder='big', signed=False)
_sdec16p1 = DecimalX('sdec16p1', nbytes=2, precision=1, byteorder='big', signed=True)
_udec16p2 = DecimalX('udec16p2', nbytes=2, precision=2, byteorder='big', signed=False)

_serial_number_t = _SerialNumberX('serial_number_t', nbytes=6)
_reserved = ArrayX('reserved', fmt=uint8)


class MicroinverterData(Structure):
    """Microinverter status data."""

    data_type: int = member(fmt=uint8)
    serial_number: str = member(fmt=_serial_number_t)
    """Microinverter serial number."""
    port_number: int = member(fmt=uint8)
    """Port number"""
    pv_voltage: Decimal = member(fmt=_udec16p1, doc='V')
    """PV voltage [V]."""
    pv_current: Decimal = member(fmt=_udec16p1, doc='A')
    """PV current [A]."""
    grid_voltage: Decimal = member(fmt=_udec16p1, doc='V')
    """Grid voltage [V]."""
    grid_frequency: Decimal = member(fmt=_udec16p2, doc='Hz')
    """Grid frequency [Hz]."""
    pv_power: Decimal = member(fmt=_udec16p1, doc='W')
    """PV power [W]"""
    today_production: int = member(fmt=uint16, doc='Wh')
    """Today production [Wh]."""
    total_production: int = member(fmt=uint32, doc='Wh')
    """Total production [Wh]."""
    temperature: Decimal = member(fmt=_sdec16p1, doc='°C')
    """Microinverter temperature [C]."""
    operating_status: int = member(fmt=uint16)
    """Operating status."""
    alarm_code: int = member(fmt=uint16)
    """Alarm code."""
    alarm_count: int = member(fmt=uint16)
    """Alarm count."""
    link_status: int = member(fmt=uint8)
    """Link status"""
    reserved: List[int] = member(fmt=_reserved)


@dataclass
class PlantData:
    """Data for the whole plant."""

    dtu: str
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

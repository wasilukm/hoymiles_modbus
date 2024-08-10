"""Tests for _CustomSocketFramer."""
from unittest.mock import patch

from hoymiles_modbus.client import _CustomSocketFramer


def test_short_frame():
    """Verify that frames shorter than 10 are not modified."""
    framer = _CustomSocketFramer(decoder=None)

    with patch('hoymiles_modbus.client.ModbusSocketFramer.processIncomingPacket') as super_process_incoming_packet:
        framer.processIncomingPacket(data=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00', callback=None, unit=0)
    super_process_incoming_packet.assert_called_once_with(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00', None, 0)


def test_long_frame():
    """Verify that frames longer than 9 have fixed length byte."""
    framer = _CustomSocketFramer(decoder=None)
    """Verify that frames longer than 9 have fixed length byte."""
    with patch('hoymiles_modbus.client.ModbusSocketFramer.processIncomingPacket') as super_process_incoming_packet:
        framer.processIncomingPacket(data=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\00', callback=None, unit=0)
    super_process_incoming_packet.assert_called_once_with(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00', None, 0)

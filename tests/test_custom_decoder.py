"""Tests for _CustomDecoder."""

from unittest.mock import patch

from hoymiles_modbus.client import _CustomDecoder


def test_short_message():
    """Verify that data shorter than 2 is not modified."""
    decoder = _CustomDecoder(is_server=False)

    with patch('hoymiles_modbus.client.DecodePDU.decode') as super_decode:
        decoder.decode(b'\x00\x00')
    super_decode.assert_called_once_with(b'\x00\x00')


def test_long_message():
    """Verify that data longer than 2 has fixed length byte."""
    decoder = _CustomDecoder(is_server=False)

    with patch('hoymiles_modbus.client.DecodePDU.decode') as super_decode:
        decoder.decode(b'\x00\x00\x00')
    super_decode.assert_called_once_with(b'\x00\x01\x00')

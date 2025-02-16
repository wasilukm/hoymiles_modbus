"""Tests for packet data size fixer.."""

from hoymiles_modbus._modbus_tcp_client import _data_size_fixer


def test_received_packed():
    """Verify that data size byte is fixed for received frames."""
    received_packet = b'12345678901234567890'
    fixed_packet = _data_size_fixer(sending=False, data=received_packet)
    assert fixed_packet == b'12345678\x0b01234567890'


def test_packets_to_sent():
    """Verify packet to sent are not modified."""
    packet_to_sent = b'12345678901234567890'
    fixed_packet = _data_size_fixer(sending=True, data=packet_to_sent)
    assert fixed_packet == packet_to_sent

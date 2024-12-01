"""Tests for PDU data size fixer.."""

from hoymiles_modbus._modbus_tcp_client import CommunicationParams, create_modbus_tcp_client


def test_data_size_fixer():
    """Verify PDU data size fixer."""
    client = create_modbus_tcp_client('127.0.0.1', port=502, comm_params=CommunicationParams())
    # should be able to decode frame even with wrong size (0xFF here)
    pdu = client.framer.decoder.decode(b'\x03\xFF\x10\xf8q`\x081')
    assert pdu.getRegister(0) == 4344
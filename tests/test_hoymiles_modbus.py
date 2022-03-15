#!/usr/bin/env python
"""Tests for `hoymiles_modbus` package."""

import pytest
from decimal import Decimal
from unittest import mock
from pymodbus.exceptions import ModbusIOException

from hoymiles_modbus import client
from hoymiles_modbus.datatypes import MISeriesMicroinverterData, HMSeriesMicroinverterData, MicroinverterType


example_raw_modbus_responses = [
    b'(\x0c\x1032\x41cU\x01\x01^\x00\x02\tM\x13\x88\x00f\x02\xef\x00\x01$G\x00+\x00\x03\x00\x00\x00\x00\x01'
    b'\x07\x00\x00\x00\x00\x00\x00',
    b'P\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00',
]


def test_microinverter_data_decode_mi_series():
    """Test decoding microinverter data."""
    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = example_raw_modbus_responses
        client_mock.read_holding_registers.return_value.isError.return_value = False
        expected = [
            MISeriesMicroinverterData(
                data_type=12,
                serial_number='103332416355',
                port_number=1,
                pv_voltage=Decimal('35'),
                pv_current=Decimal('0.2'),
                grid_voltage=Decimal('238.1'),
                grid_frequency=Decimal('50'),
                pv_power=Decimal('10.2'),
                today_production=751,
                total_production=74823,
                temperature=Decimal('4.3'),
                operating_status=3,
                alarm_code=0,
                alarm_count=0,
                link_status=1,
                reserved=[7, 0, 0, 0, 0, 0, 0],
            )
        ]
        microinverter_data = client.HoymilesModbusTCP('1.2.3.4').microinverter_data
        assert microinverter_data == expected


def test_microinverter_data_decode_hm_series():
    """Test decoding microinverter data."""
    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = example_raw_modbus_responses
        client_mock.read_holding_registers.return_value.isError.return_value = False
        expected = [
            HMSeriesMicroinverterData(
                data_type=12,
                serial_number='103332416355',
                port_number=1,
                pv_voltage=Decimal('35'),
                pv_current=Decimal('0.02'),
                grid_voltage=Decimal('238.1'),
                grid_frequency=Decimal('50'),
                pv_power=Decimal('10.2'),
                today_production=751,
                total_production=74823,
                temperature=Decimal('4.3'),
                operating_status=3,
                alarm_code=0,
                alarm_count=0,
                link_status=1,
                reserved=[7, 0, 0, 0, 0, 0, 0],
            )
        ]
        microinverter_data = client.HoymilesModbusTCP(
            '1.2.3.4', microinverter_type=MicroinverterType.HM
        ).microinverter_data
        assert microinverter_data == expected


def test_unknown_microinverter_type():
    """Test exception for unknown microinverter type."""
    with pytest.raises(ValueError):
        client.HoymilesModbusTCP('1.2.3.4', microinverter_type='foo')


def test_stop_microinverter_data_decode_on_empty_serial():
    """Verify that requesting microinverter register stops on receiving first empty serial number."""
    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = example_raw_modbus_responses + [
            b'(\x0c\x1032\x41cU\x01\x01^\x00\x02\tM\x13\x88\x00f\x02\xef\x00\x01$G\x00+\x00\x03\x00\x00\x00\x00\x01'
            b'\x07\x00\x00\x00\x00\x00\x00']
        client_mock.read_holding_registers.return_value.isError.return_value = False
        assert len(client.HoymilesModbusTCP('1.2.3.4').microinverter_data) == 1


def test_dtu():
    """Test decoding DTU serial number."""
    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = [b'\x06\x11\xd3a`\x081']
        client_mock.read_holding_registers.return_value.isError.return_value = False
        assert client.HoymilesModbusTCP('1.2.3.4').dtu == '11d361600831'


example_microinverter_data = [
    MISeriesMicroinverterData(  # type: ignore[call-overload]
        data_type=12,
        serial_number='103332416355',
        port_number=1,
        pv_voltage=Decimal('35'),
        pv_current=Decimal('0.2'),
        grid_voltage=Decimal('238.1'),
        grid_frequency=Decimal('50'),
        pv_power=Decimal('10.2'),
        today_production=751,
        total_production=74823,
        temperature=Decimal('4.3'),
        operating_status=3,
        alarm_code=0,
        alarm_count=0,
        link_status=1,
        reserved=[7, 0, 0, 0, 0, 0, 0],
    ),
    MISeriesMicroinverterData(  # type: ignore[call-overload]
        data_type=12,
        serial_number='117763504101',
        port_number=1,
        pv_voltage=Decimal('34.8'),
        pv_current=Decimal('0.2'),
        grid_voltage=Decimal('237.9'),
        grid_frequency=Decimal('50'),
        pv_power=Decimal('9.9'),
        today_production=679,
        total_production=54328,
        temperature=Decimal('6'),
        operating_status=3,
        alarm_code=0,
        alarm_count=0,
        link_status=1,
        reserved=[7, 0, 0, 0, 0, 0, 0],
    ),
]


def test_plant_data():
    """Test calculated values in plant data."""
    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        with mock.patch.object(
            client.HoymilesModbusTCP, 'dtu', new_callable=mock.PropertyMock, return_value='11d361600831'
        ):
            with mock.patch.object(
                client.HoymilesModbusTCP,
                'microinverter_data',
                new_callable=mock.PropertyMock,
                return_value=example_microinverter_data,
            ):
                plant_data = client.HoymilesModbusTCP('1.2.3.4').plant_data
                assert plant_data.dtu == '11d361600831'
                assert plant_data.today_production == 1430
                assert plant_data.total_production == 129151


def test_no_alarm():
    """Test inactive alarm in plant data."""
    for data in example_microinverter_data:
        data.alarm_code = 0

    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        with mock.patch.object(
            client.HoymilesModbusTCP, 'dtu', new_callable=mock.PropertyMock, return_value='11d361600831'
        ):
            with mock.patch.object(
                client.HoymilesModbusTCP,
                'microinverter_data',
                new_callable=mock.PropertyMock,
                return_value=example_microinverter_data,
            ):
                plant_data = client.HoymilesModbusTCP('1.2.3.4').plant_data
                assert plant_data.alarm_flag is False


def test_alarm():
    """Test active alarm in plant data."""
    example_microinverter_data[0].alarm_code = 1

    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        with mock.patch.object(
            client.HoymilesModbusTCP, 'dtu', new_callable=mock.PropertyMock, return_value='11d361600831'
        ):
            with mock.patch.object(
                client.HoymilesModbusTCP,
                'microinverter_data',
                new_callable=mock.PropertyMock,
                return_value=example_microinverter_data,
            ):
                plant_data = client.HoymilesModbusTCP('1.2.3.4').plant_data
                assert plant_data.alarm_flag is True


def test_modbus_response_exception():
    """Verify that exception is raised when error in modbus response."""
    client_mock = mock.Mock()
    with mock.patch.object(client.ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value = ModbusIOException()
        with pytest.raises(ModbusIOException):
            client.HoymilesModbusTCP('1.2.3.4').dtu

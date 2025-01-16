#!/usr/bin/env python
"""Tests for `hoymiles_modbus` package."""
from decimal import Decimal
from unittest import mock

import pytest

from hoymiles_modbus._modbus_tcp_client import ModbusTcpClient
from hoymiles_modbus.client import HoymilesModbusTCP
from hoymiles_modbus.datatypes import InverterData

example_mi_series_raw_responses = [
    b'(\x0c\x1032\x41cU\x01\x01^\x00\x02\tM\x13\x88\x00f\x02\xef\x00\x01$G\x00+\x00\x03\x00\x00\x00\x00\x01'
    b'\x07\x00\x00\x00\x00\x00\x00',
    b'P\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00',
]

example_hm_series_raw_responses = [
    b'(\x0c\x1132\x41cU\x01\x01^\x00\x02\tM\x13\x88\x00f\x02\xef\x00\x01$G\x00+\x00\x03\x00\x00\x00\x00\x01'
    b'\x07\x00\x00\x00\x00\x00\x00',
    b'P\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00',
]


example_unknown_series_raw_responses = [
    b'(\x0c\x1232\x41cU\x01\x01^\x00\x02\tM\x13\x88\x00f\x02\xef\x00\x01$G\x00+\x00\x03\x00\x00\x00\x00\x01'
    b'\x07\x00\x00\x00\x00\x00\x00',
    b'P\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00',
]


def test_inverter_data_decode_mi_series():
    """Test decoding MI series inverter data."""
    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = example_mi_series_raw_responses
        client_mock.read_holding_registers.return_value.isError.return_value = False
        expected = [
            InverterData(
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
        inverters_data = HoymilesModbusTCP('1.2.3.4').inverters
        assert inverters_data == expected


def test_inverter_data_decode_hm_series():
    """Test decoding HM inverter data."""
    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = example_hm_series_raw_responses
        client_mock.read_holding_registers.return_value.isError.return_value = False
        expected = [
            InverterData(
                data_type=12,
                serial_number='113332416355',
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
        inverters_data = HoymilesModbusTCP('1.2.3.4').inverters
        assert inverters_data == expected


def test_stop_inverter_data_decode_on_empty_serial():
    """Verify that inverters data gathering stops on receiving first empty serial number."""
    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = example_mi_series_raw_responses + [
            b'(\x0c\x1032\x41cU\x01\x01^\x00\x02\tM\x13\x88\x00f\x02\xef\x00\x01$G\x00+\x00\x03\x00\x00\x00\x00\x01'
            b'\x07\x00\x00\x00\x00\x00\x00'
        ]
        client_mock.read_holding_registers.return_value.isError.return_value = False
        assert len(HoymilesModbusTCP('1.2.3.4').inverters) == 1


def test_dtu():
    """Test decoding DTU serial number."""
    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = [b'\x06\x11\xd3a`\x081']
        client_mock.read_holding_registers.return_value.isError.return_value = False
        assert HoymilesModbusTCP('1.2.3.4').dtu == '11d361600831'


example_inverters_data = [
    InverterData(  # type: ignore[call-overload]
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
    InverterData(  # type: ignore[call-overload]
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
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        with mock.patch.object(HoymilesModbusTCP, 'dtu', new_callable=mock.PropertyMock, return_value='11d361600831'):
            with mock.patch.object(
                HoymilesModbusTCP,
                'inverters',
                new_callable=mock.PropertyMock,
                return_value=example_inverters_data,
            ):
                plant_data = HoymilesModbusTCP('1.2.3.4').plant_data
                assert plant_data.dtu == '11d361600831'
                assert plant_data.today_production == 1430
                assert plant_data.total_production == 129151


def test_no_alarm():
    """Test inactive alarm in plant data."""
    for data in example_inverters_data:
        data.alarm_code = 0

    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        with mock.patch.object(HoymilesModbusTCP, 'dtu', new_callable=mock.PropertyMock, return_value='11d361600831'):
            with mock.patch.object(
                HoymilesModbusTCP,
                'inverters',
                new_callable=mock.PropertyMock,
                return_value=example_inverters_data,
            ):
                plant_data = HoymilesModbusTCP('1.2.3.4').plant_data
                assert plant_data.alarm_flag is False


def test_alarm():
    """Test active alarm in plant data."""
    example_inverters_data[0].alarm_code = 1

    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        with mock.patch.object(HoymilesModbusTCP, 'dtu', new_callable=mock.PropertyMock, return_value='11d361600831'):
            with mock.patch.object(
                HoymilesModbusTCP,
                'inverters',
                new_callable=mock.PropertyMock,
                return_value=example_inverters_data,
            ):
                plant_data = HoymilesModbusTCP('1.2.3.4').plant_data
                assert plant_data.alarm_flag is True


def test_modbus_response_exception():
    """Verify that exception is raised when error in modbus response."""
    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        response = mock.Mock()
        response.isError.return_value = True
        client_mock.read_holding_registers.return_value = response
        with pytest.raises(RuntimeError):
            _ = HoymilesModbusTCP('1.2.3.4').dtu


def test_exception_when_no_inverters():
    """Test exception when there are no inverters."""
    client_mock = mock.Mock()
    with mock.patch.object(ModbusTcpClient, '__enter__', return_value=client_mock):
        client_mock.read_holding_registers.return_value.encode.side_effect = [b'']
        client_mock.read_holding_registers.return_value.isError.return_value = False
        hoymiles_modbus_tcp = HoymilesModbusTCP('1.2.3.4')
        with pytest.raises(RuntimeError) as err:
            _ = hoymiles_modbus_tcp.inverters
        assert str(err.value) == "Inverters not mapped yet."

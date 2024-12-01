# Changelog

## [0.8.0] (2024-12-01)

Features:
 * support for automatic detection of inverter type
 * exposed reconnect_delay_max connection parameter

Breaking changes:
* support for pymodbus 3.7, dropped support for older versions
* `CommunicationParams` class moved to `hoymiles_modbus.datatypes`
* connection parameters: `retry_on_empty`, `close_comm_on_error` and `strict` are no longer supported
* removed `microinverter_type` parameter from `HoymilesModbusTCP`
* data structures `MISeriesMicroinverterData` and `HMSeriesMicroinverterData` replaced by `InverterData`
* renamed `PlantData.microinverter_data` to `PlantData.inverters`
* renamed `HoymilesModbusTCP.microinverter_data` to `HoymilesModbusTCP.inverters`


## [0.7.0] (2024-08-12)

* add support for Python 3.12
* BREAKING CHANGE: drop support for Python 3.8


## [0.6.3] (2024-08-10)

* prevent installing pymodbus 3.7 and greater which has broken backward compatibility
* don't treat modbus response as an exception, instead raise RuntimeError for negative response

## [0.6.2] (2023-03-05)

* only documentation changes
    * fix generating API documentation
    * extend usage examples

## [0.6.1] (2023-02-26)

* Raise RuntimeError when trying to read microinverters, but they are not added yet in DTU

## [0.6.0] (2023-02-07)

* add support for Python 3.10 and 3.11
* remove support for Python 3.6 and 3.7

## [0.5.0] (2022-10-03)

* Add support for low level pymodbus communication parameters. A user can configure additional
  communication parameters via `HoymilesModbusTCP().comm_params`

## [0.4.0] (2022-05-07)

* Add support for custom Modbus Unit ID
* Bump plum-py version

## [0.2.1] (2022-04-23)

* Again fix handling modbus exceptions - modbus error was
  causing `IndexError: list assignment index out of range` exception

## [0.2.0] (2022-03-15)

* improve modbus exception handling - now when there is an error in
  a response then pymodbus exception is raised
* add support for HM microinverter series - previously `pv_current`
  was incorrectly interpreted for these microinverters

## [0.1.0] (2022-03-12)

* First release on PyPI.

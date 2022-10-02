# Changelog

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

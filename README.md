# hoymiles_modbus


[![pypi](https://img.shields.io/pypi/v/hoymiles_modbus.svg)](https://pypi.org/project/hoymiles_modbus/)
[![python](https://img.shields.io/pypi/pyversions/hoymiles_modbus.svg)](https://pypi.org/project/hoymiles_modbus/)
[![Build Status](https://github.com/wasilukm/hoymiles_modbus/actions/workflows/dev.yml/badge.svg)](https://github.com/wasilukm/hoymiles_modbus/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/wasilukm/hoymiles_modbus/branch/main/graphs/badge.svg)](https://codecov.io/github/wasilukm/hoymiles_modbus)



Python library for gathering data from Hoymiles microinverters.

The library communicates with DTU (DTU-Pro) which is a proxy/monitoring device for microinverters.
DTU should be connected via its `Ethernet` port and should have IP address assigned by DHCP server.


* Documentation: <https://wasilukm.github.io/hoymiles_modbus>
* GitHub: <https://github.com/wasilukm/hoymiles_modbus>
* PyPI: <https://pypi.org/project/hoymiles_modbus/>
* Free software: MIT


## Features

* Communication via Modbus TCP
* Decode all microinverter status registers, which include information such as:
  * current production
  * total production
  * today production
  * temperature
  * alarms
  * status
  * grid voltage and frequency

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.

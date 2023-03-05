# Usage

To use hoymiles_modbus in a project

```
from hoymiles_modbus.client import HoymilesModbusTCP

plant_data = HoymilesModbusTCP('1.2.3.4').plant_data
print(plant_data.today_production)

```

The above example assumes `MI` inverters, for `HM` change type as below:

```
from hoymiles_modbus.client import HoymilesModbusTCP
from hoymiles_modbus.datatypes import MicroinverterType

plant_data = HoymilesModbusTCP(
    '1.2.3.4', microinverter_type=MicroinverterType.HM).plant_data
print(plant_data.today_production)


```

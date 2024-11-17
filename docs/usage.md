# Usage

To use hoymiles_modbus in a project

```
from hoymiles_modbus.client import HoymilesModbusTCP

plant_data = HoymilesModbusTCP('1.2.3.4').plant_data
print(plant_data.today_production)

```

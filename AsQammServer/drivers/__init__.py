#######################################
#  Импортируем драйвера Arduino-плат  #
#######################################

from .arduboards.arduinounor3  import AqArduinoUnoR3
from .arduboards.seeeduinov4bs import AqSeeeduinoV4WithBaseShield

#######################################
#     Импортируем Arduino-сенсоры     #
#######################################

from .ardusensors.groveTS12    import GroveTemperatureSensor
from .ardusensors.soilmst      import CapacitiveSoilMoistureSensor

#######################################
#   Импортируем Arduino-исполнители   #
#######################################

from .arduexecutors.d13led     import D13LED

#######################################
#         Индексируем драйвера        #
#######################################

Boards      = {1071:              AqArduinoUnoR3,
                   1072:              AqSeeeduinoV4WithBaseShield}

Modules     = {1101:              GroveTemperatureSensor,
                   1102:              CapacitiveSoilMoistureSensor,
                   1000:              D13LED}

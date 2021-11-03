using System;

using AsQammServer;
using AsQammServer.Hardware;
using AsQammServer.Drivers;

using Solid.Arduino;


namespace AsQammServer.Drivers
{
    public class ArduinoUnoR3: ArduinoDevice
    {
        public ArduinoUnoR3(
            bool isEnabled,
            string comPort,
            SerialBaudRate baudRate,
            string instanceName,
            string instanceDescription):
            
            base(isEnabled, comPort, "AUR3", baudRate, displayData: 
                new DeviceDisplayData(
                    "Arduino Uno R3", "Arduino Uno board",
                    instanceName, instanceDescription))
        {

        }
    }
}

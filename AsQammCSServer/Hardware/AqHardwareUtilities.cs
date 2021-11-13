using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using AsQammServer.Client;


namespace AsQammServer.Hardware
{
    public static class HardwareExtensions
    {
        public static string ToString(this AqAbstractDevice.ConnectionType self)
        {
            switch (self)
            {
                case AqAbstractDevice.ConnectionType.WireGeneric:
                    return "Wire (unknown subtype)";

                case AqAbstractDevice.ConnectionType.WireSerial:
                    return "Wire: Serial";

                case AqAbstractDevice.ConnectionType.WireFirmata:
                    return "Wire: Firmata";

                case AqAbstractDevice.ConnectionType.WirelessWiFi:
                    return "Wireless: WiFi";

                case AqAbstractDevice.ConnectionType.WirelessBluetooth:
                    return "Wireless: Bluetooth";

                case AqAbstractDevice.ConnectionType.WirelessMobile:
                    return "Wireless: Mobile (Cellular)";

                default:
                    return "Unknown";
            }
        }
    }
}

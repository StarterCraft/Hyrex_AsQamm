using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Reflection;


namespace AsQammServer.DriverControl
{
    /// <summary>
    /// Класс для работы с драйверами протоколов и устройств.
    /// </summary>
    public static class DriverManager
    {
        public static Dictionary<string, List<Type>> Platforms = new();
        public static List<Type> Devices = new();


        public static Type GetDeviceClass(string platformName, string className)
        {
            return Platforms[platformName].Where(device => device.Name == className).First();
        }
    }
}

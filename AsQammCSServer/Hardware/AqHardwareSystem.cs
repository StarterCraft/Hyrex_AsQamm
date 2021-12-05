using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Threading.Tasks;
using System.Reflection;
using Microsoft.Extensions.Configuration;

using NLog;

using Newtonsoft.Json;

using AsQammServer.Utilities;
using AsQammServer.DriverControl;


namespace AsQammServer.Hardware
{
    /// <summary>
    /// Класс системы управления оборудованием. Она осуществляет инициализацию
    /// всех исполнителей и комплексов; занимается мониторингом (записью
    /// значений) датчиков; осуществляет следование правилам (отдаёт команды
    /// исполнителям, работающим на вывод, в соответствии с ними).
    /// </summary>
    public class AqHardwareSystem
    {
        private Logger Logger = LogManager.GetLogger("Hardware");

        public const string ConfigurationFilePath = "SystemProperties\\Hardware.asqd";
        private IConfigurationRoot Configuration;

        public bool IsOK = new();
        public Dictionary<string, List<AqAbstractDevice>> InstalledHardware = new();

        public dynamic Statist;


        /// <summary>
        /// Инициализировать драйверы протоколов.
        /// </summary>
        public void LoadPlatformDrivers()
        {
            int count = 0;

            foreach (string fileName in Directory.GetFiles(
                $"{Directory.GetCurrentDirectory()}\\Drivers\\Platforms", "*.dll",
                SearchOption.TopDirectoryOnly))
            {
                string platformName = fileName.Split('\\').Last().SubstringN(0, -3);
                List<string> classNames = new();
                List<Type> types = Assembly.LoadFile(fileName).GetExportedTypes().ToList();

                foreach (Type type in types)
                {
                    if (type.IsSubclassOf(typeof(AqAbstractDevice)))
                    {
                        count++;
                        classNames.Add(type.Name);
                        Logger.Debug(
                            $"Класс протокола {platformName} " +
                            $"{type.Name} инициализирован");
                    }
                }

                if (classNames.Count() != 0)
                    DriverManager.Platforms.Add(platformName, new List<Type>());

                foreach (string className in classNames)
                    DriverManager.Platforms[platformName].Add(types.Single(t => t.Name == className));
            }

            Logger.Info($"Инициализировано {count} дрйверов протоколов");
        }


        /// <summary>
        /// Инициализировать драйверы устройств.
        /// </summary>
        public void LoadDeviceDrivers()
        {
            foreach (string folderName in Directory.GetDirectories(
                "Drivers\\Devices", "*", SearchOption.TopDirectoryOnly))
            {
                if (folderName.Contains('.')) continue;

                foreach (string installedPlatformName in DriverManager.Platforms.Keys)
                {
                    if (folderName.Contains(installedPlatformName))
                    {
                        Dictionary<string, List<string>> deviceDriverClasses = new();

                        foreach (string fileName in Directory.GetFiles(
                            folderName, "*.dll", SearchOption.AllDirectories))
                        {
                            List<Type> types = Assembly.LoadFile(fileName).GetExportedTypes().ToList();

                            foreach (Type type in types)
                            {
                                if (typeof(AqAbstractDevice).IsAssignableFrom(type))
                                {
                                    if (!deviceDriverClasses.Keys.Contains(fileName))
                                        deviceDriverClasses.Add(fileName, new List<string>());

                                    deviceDriverClasses[fileName].Add(type.Name);
                                    Logger.Debug($"Класс протокола {type.Name} инициализирован");
                                }

                                else continue;
                            }
                        }

                        foreach (KeyValuePair<string, List<string>> pair in deviceDriverClasses)
                        {
                            List<Type> types = Assembly.LoadFile(pair.Key).GetExportedTypes().ToList();

                            foreach (string className in pair.Value) 
                                DriverManager.Devices.Add(types.Single(t => t.Name == className));
                        }
                    }
                }
            }
        }


        /// <summary>
        /// Инициализировать устройства
        /// </summary>
        public void InitializeDevices() 
        { 

        }


        public AqHardwareSystem()
        {
            //Инициализация протоколов
            Logger.Info("Инициализация протоколов...");
            LoadPlatformDrivers();

            //Инициализация драйверов
            Logger.Info("Инициализация драйверов устройств...");
            LoadDeviceDrivers();

            //Инициализация устройств
            Logger.Info("Инициализация устройств");

        }
    }
}

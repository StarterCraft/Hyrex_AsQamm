using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.IO;

using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;

using NLog;

using AsQammServer.Utilities;


namespace AsQammServer
{
    public class Server
    {
        private static readonly Logger Logger = NLog.LogManager.GetLogger("Server");

        public const string ConfigurationFilePath = "SystemProperties\\General.asqd";

        public static void Main(string[] args)
        {
            AqLogger.GlobalConfiguration(LogLevel.Debug, LogLevel.Debug);

            CheckNecessaryPaths();

            Hardware.AqHardwareSystem hardware = new Hardware.AqHardwareSystem();

            CreateHostBuilder(args).Build().Run();
        }


        /// <summary>
        /// Проверить, существуют ли необходимые для работы файлы и папки, если
        /// нет, то создать их
        /// </summary>
        public static void CheckNecessaryPaths()
        {
            List<string> environment;

            List<string> requiredFolders = new()
            {
                "Drivers\\Platforms",
                "Drivers\\Devices",
                "Personal",
                "SystemProperties"
            };

            List<string> requiredFiles = new()
            {
                //Основные настройки
                "SystemProperties\\General.asqd",

                //Настройки устройств
                "SystemProperties\\Hardware.asqd",

                //Настройки комплексов
                "SystemProperties\\Complex.asqd",

                //Регистр пользователей
                "SystemProperties\\FfReg.asqd",

                //Файл профиля гостя
                "Personal\\Guest.asqd"
            };


            //Проверим папки
            environment = Directory.GetDirectories(Directory.GetCurrentDirectory()).ToList();
            foreach (string folderName in requiredFolders)
            {
                //Если папка с именем folderName не существует,
                //то создать папку с таким именем.
                if (!environment.Contains($"{Directory.GetCurrentDirectory()}\\{folderName}"))
                    Directory.CreateDirectory(folderName);
            }

            //Проверим файлы
            environment = Directory.GetFiles(Directory.GetCurrentDirectory(), "*.*", SearchOption.AllDirectories).ToList();
            foreach (string fileName in requiredFiles)
            {
                if (!(environment.Contains(fileName)))
                {
                    using (StreamWriter file = File.CreateText(fileName)) file.WriteLine("");
                }
            }
        }


        /// <summary>
        /// Инициализатор сборщика хоста
        /// </summary>
        /// <param name="args"></param>
        /// <returns></returns>
        public static IHostBuilder CreateHostBuilder(string[] args)
        {
            IHostBuilder builder;

            builder = Host.CreateDefaultBuilder(args);
            builder.ConfigureWebHostDefaults(web => web.UseStartup<Startup>());

            return builder;
        }
    }
}

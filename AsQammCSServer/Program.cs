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
        /// ���������, ���������� �� ����������� ��� ������ ����� � �����, ����
        /// ���, �� ������� ��
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
                //�������� ���������
                "SystemProperties\\General.asqd",

                //��������� ���������
                "SystemProperties\\Hardware.asqd",

                //��������� ����������
                "SystemProperties\\Complex.asqd",

                //������� �������������
                "SystemProperties\\FfReg.asqd",

                //���� ������� �����
                "Personal\\Guest.asqd"
            };


            //�������� �����
            environment = Directory.GetDirectories(Directory.GetCurrentDirectory()).ToList();
            foreach (string folderName in requiredFolders)
            {
                //���� ����� � ������ folderName �� ����������,
                //�� ������� ����� � ����� ������.
                if (!environment.Contains($"{Directory.GetCurrentDirectory()}\\{folderName}"))
                    Directory.CreateDirectory(folderName);
            }

            //�������� �����
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
        /// ������������� �������� �����
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

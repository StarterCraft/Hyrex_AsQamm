using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

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

        public static void Main(string[] args)
        {
            AqLogger.GlobalConfiguration(LogLevel.Debug, LogLevel.Debug);
            //CreateHostBuilder(args).Build().Run();
            Hardware.AqHardwareSystem hardware = new Hardware.AqHardwareSystem();
        }


        public static IHostBuilder CreateHostBuilder(string[] args)
        {
            IHostBuilder builder;

            builder = Host.CreateDefaultBuilder(args);
            builder.ConfigureWebHostDefaults(web => web.UseStartup<Startup>());

            return builder;
        }
    }
}

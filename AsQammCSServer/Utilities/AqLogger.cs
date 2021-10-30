using System;

using NLog;


namespace AsQammServer.Utilities
{
    /// <summary>
    /// Класс канала журналирования.
    /// </summary>
    /// Журналирование необходимо для отборажения пользователю информацию о
    /// текущих действиях сервера, сообщения о предупреждениях и об ошибках.
    /// 
    /// Каналов журналирования(или `логгеров`) может быть сколько угодно.
    /// При этом итоговый журнал всегда сохраняется в ОДИН файл, имя которого
    /// определяется при запуске самого ПЕРВОГО канала журналирования.
    /// 
    /// Каждый из этих каналов имеет своё имя и настраивается по уровню жур-
    /// налирования (насколько важные сообщения нужно выводить в консоль и
    /// сохранять в журнал?).
    /// 
    /// Любые файлы журналов сохраняются в папке '{папка местонаждения программы}/logs'.
    public class AqLogger
    {
        public static readonly NLog.Config.LoggingConfiguration loggingConfiguration = new();
        public static readonly string LogFileName = $"logs/{DateTime.Now.ToString("ddMMMyyyy")}_AsQammLog.Log";


        public static void GlobalConfiguration(
            LogLevel minimumConsoleLevel,
            LogLevel minimumLogFileLevel
            )
        {
            NLog.Targets.ColoredConsoleTarget consoleTarget = new() { 
                Layout = "[${logger} @ ${level:uppercase=true}] ${message}"
            };

            NLog.Targets.FileTarget fileTarget = new()
            {
                FileName = LogFileName
            };

            loggingConfiguration.AddRule(minimumConsoleLevel, LogLevel.Fatal, consoleTarget);
            loggingConfiguration.AddRule(minimumLogFileLevel, LogLevel.Fatal, fileTarget);

            LogManager.Configuration = loggingConfiguration;
        }
    }
}

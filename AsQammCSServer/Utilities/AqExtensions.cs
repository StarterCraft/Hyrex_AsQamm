using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.Extensions.Configuration;

using Useful.Extensions;


namespace AsQammServer.Utilities
{
    public static class AqExtensions
    {
        /// <summary>
        /// Разрезать строку по отрицательным индексам.
        /// </summary>
        /// <param name="startIndex">Начальный индекс</param>
        /// <param name="endIndex">Конечный индекс</param>
        /// <returns></returns>
        public static string SubstringN(this string self, int startIndex, int endIndex)
        {
            if (startIndex >= 0 && endIndex < 0) return self.Substring(startIndex, self.Length + endIndex);
            if (startIndex < 0 && endIndex < 0) return self.Substring(self.Length - startIndex, self.Length - endIndex);

            return self.Substring(startIndex, endIndex);
        }


        /// <summary>
        /// Appends a value to the end of the sequence in place.
        /// </summary>
        public static void AppendInPlace<T>(this IEnumerable<T> self, T value)
        {
            self = self.Append(value);
        }


        /// <summary>
        /// Получить корень конфигурации из JSON-файла
        /// </summary>
        /// <param name="fileName">Имя файла</param>
        /// <returns>Корень конфигурации</returns>
        public static IConfigurationRoot GetJsonConfiguration(string fileName)
        {
            try
            {
                return new ConfigurationBuilder().AddJsonFile(fileName, true).Build();
            }

            catch (FormatException)
            {
                using (StreamWriter file = File.CreateText(fileName)) file.WriteLine("{\n    \n}");
                return new ConfigurationBuilder().AddJsonFile(fileName, true).Build();
            }
        }
    }
}

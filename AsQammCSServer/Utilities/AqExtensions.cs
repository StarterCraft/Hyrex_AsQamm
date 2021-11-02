using System.Collections.Generic;
using System.Linq;

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


        /// <inheritdoc/>
        public static void AppendInPlace<T>(this IEnumerable<T> self, T value)
        {
            self = self.Append(value);
        }
    }
}

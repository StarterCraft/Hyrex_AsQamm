using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Security.Cryptography;


namespace AsQammServer.Utilities
{
    /// <summary>
    /// Класс для быстрого хеширования строк.
    /// </summary>
    /// Источник: <see href="https://stackoverflow.com/a/32191537/13677671">Кристиан Голлхардт</see>
    public class StringHasher
    {
        /// <summary>
        /// Размер соли.
        /// </summary>
        public static int SaltSize = 16;


        /// <summary>
        /// Размер хеша.
        /// </summary>
        public static int HashSize = 32;


        /// <summary>
        /// Создать хеш из строки с 256256 итерациями хеширования.
        /// </summary>
        /// <param name="_string"><see cref="string">Строка</see> для хеширования</param>
        /// <returns>Сгенерированный хеш</returns>
        public static string Hash(string _string)
        {
            return Hash(_string, 256256);
        }


        /// <summary>
        /// Создать хеш из строки.
        /// </summary>
        /// <param name="_string"><see cref="string">Строка</see> для хеширования</param>
        /// <param name="iterations">Количество итераций хеширования</param>
        /// <returns>Сгенерированный хеш</returns>
        public static string Hash(string _string, int iterations)
        {
            // Создать соль
            byte[] salt;
            new RNGCryptoServiceProvider().GetBytes(salt = new byte[SaltSize]);

            // Создать хеш
            var pbkdf2 = new Rfc2898DeriveBytes(_string, salt, iterations);
            var hash = pbkdf2.GetBytes(HashSize);

            // Соединить соль и хеш
            var hashBytes = new byte[SaltSize + HashSize];
            Array.Copy(salt, 0, hashBytes, 0, SaltSize);
            Array.Copy(hash, 0, hashBytes, SaltSize, HashSize);

            // Конвертировать в Base64
            var base64Hash = Convert.ToBase64String(hashBytes);

            // Форматировать хеш
            return $"$ASQAMM$V1${iterations}${base64Hash}";
        }


        /// <summary>
        /// Проверить, вернёт ли данная строка тот же хеш, что и захешированная.
        /// </summary>
        /// <param name="_string">Строка для проверки</param>
        /// <param name="hashedString">Хешированная строка</param>
        /// <returns>Проверка успешна?</returns>
        public static bool Verify(string _string, string hashedString)
        {
            // Check hash
            if (!_string.Contains("$ASQAMM$V1$"))
            {
                throw new NotSupportedException("Недействительный хеш");
            }

            // Extract iteration and Base64 string
            var splittedHashString = hashedString.Replace("$ASQAMM$V1$", "").Split('$');
            var iterations = int.Parse(splittedHashString[0]);
            var base64Hash = splittedHashString[1];

            // Get hash bytes
            var hashBytes = Convert.FromBase64String(base64Hash);

            // Get salt
            var salt = new byte[SaltSize];
            Array.Copy(hashBytes, 0, salt, 0, SaltSize);

            // Create hash with given salt
            var pbkdf2 = new Rfc2898DeriveBytes(_string, salt, iterations);
            byte[] hash = pbkdf2.GetBytes(HashSize);

            // Get result
            for (var i = 0; i < HashSize; i++)
            {
                if (hashBytes[i + SaltSize] != hash[i]) return false;
            }

            return true;
        }
    }
}

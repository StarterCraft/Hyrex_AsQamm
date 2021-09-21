using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text;
using System.Security.Cryptography;


namespace AsQammServer.Utilities
{
    /// <summary>
    /// Статический класс для работы с криптографией.
    /// </summary>
    public static class AqCrypto
    {
        /// <summary>
        /// Преобразовать обыкновенную строку в зашифрованную Base64-строку.
        /// </summary>
        /// <param name="text">Обыкновенная <see cref="String">строка</see> для зашифровки</param>
        /// <returns>Зашифрованная Base-64 <see cref="String">строка</see></returns>
        public static string EncryptBase64(string text)
        {
            return Convert.ToBase64String(Encoding.UTF8.GetBytes(text));
        }


        /// <summary>
        /// Преобразовать зашифрованную Base-64 строку в обыкновенную.
        /// </summary>
        /// <param name="text">Зашифрованная Base-64 <see cref="String">строка</see></param>
        /// <returns>Расшифрованная из Base-64 <see cref="String">строка</see></returns>
        public static string DecryptBase64(string text)
        {
            return Encoding.UTF8.GetString(Convert.FromBase64String(text));
        }
    }
}

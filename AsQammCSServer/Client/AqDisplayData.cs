using System;
using System.Runtime.Serialization;


namespace AsQammServer.Client
{
    /// <summary>
    /// Шаблон класса с информацией о каком-либо объекте системы
    /// для отображения в вершителях.
    /// </summary>
    public abstract class AqDisplayData
    {
        /// <summary>
        /// Отображаемое имя типа объекта
        /// </summary>
        public string TypeDisplayName;

        /// <summary>
        /// Описание типа объекта
        /// </summary>
        public string TypeDescription;

        /// <summary>
        /// Отображаемое имя конкретного объекта. Может быть пустым
        /// </summary>
        public string InstanceName;

        /// <summary>
        /// Описание конкретного объекта. Может быть пустым
        /// </summary>
        public string InstanceDescription;
    }
}

﻿using System.Collections.Generic;


namespace AsQammServer.Hardware
{
    /// <summary>
    /// Интерфейс, представляющий любого `объекта` (или, упрощённо, `устройство`)
    /// — устройство, находящееся в подчинении сервера.
    /// </summary>
    /// Все классы поддерживаемых типов устройств-исполнителей являются реализациями 
    /// этого интерфейса. `Исполнители` и `устройства` есть одно и то же, если не 
    /// указано иное! `Устройства` могут иметь подчинённых себе других `устройств`, 
    /// если это предусмотрено типом устройства. Они могут быть объединены в `комплексы`
    /// для более глубокого взаимодействия друг с другом.
    ///
    ///Информация о них находится в hardware.asqd в виде JSON-списка по схеме ниже.
    ///Там хранятся базовые настройки устройства, а также информация обо всех под-
    ///чинённых ему устройствах и их настройках:
    ///
    /// [
    ///     /*Объект устройства, где:
    ///       a —— ID драйвера устройства (любой ID драйвера представляет из себя
    ///        строку длиной 4 символа, состоящую из символов латиницы и цифр
    ///        от 0 до 9);
    ///       b —— адрес (его форма зависит от типа объекта), на котором он
    ///        располагается;
    ///       c —— Настройки объекта в виде "имя параметра: значение";
    ///       d —— какой-либо определитель способа подключения к подчинённому ис-
    ///        полнителю (например, для Arduino-объекта — адрес пина, на
    ///        котором располагается подчинённый исполнитель);
    ///       e —— ID драйвера подчинённого объекта;
    ///       f —— Настройки подчинённого объекта в виде 
    ///        "имя параметра: значение"
    ///     */
    ///     
    ///     [a, b, {
    ///         c,
    ///         "children": {
    ///         //В параметре children хранится информация о подчинённых испол-
    ///         //нителях, привязанных к исполнителю, если они им поддержива-
    ///         //ются
    ///             d: [e, {
    ///                 f
    ///                 },
    ///     
    ///                 //другие определения подчинённых исполнителей по той же схеме
    ///             }
    ///         }
    ///     ],
    ///     
    ///     //другие определения исполнителей по той же схеме
    /// ]
    public interface IAqDevice
    {
        /// <summary>
        /// Перечисление возможных способов подключения к какому-то исполнителю.
        /// </summary>
        public enum ConnectionType
        {
            WireSerial = 1,
            WireFirmata = 2,
            WirelessWiFi = 3,
            WirelessBluetooth = 4,
            WirelessMobile = 5
        }


        /// <summary>
        /// Если исполнитель является подчинённым, то в этом атрибуте будет нахо-
        /// диться ссылка на объект материнского объекта, иначе — null
        /// </summary>
        public IAqDevice Parent 
        { 
            get; set;
        }

        /// <summary>
        /// Список подчинённых исполнителей этого исполнителя. Не инициализируется,
        /// если исполнитель не может иметь подчинённых исполнителей
        /// </summary>
        public List<IAqDevice> Children 
        {
            get; set;
        }

        public bool CanRetrieve
        {
            get; set;
        }

        public bool CanExecute
        {
            get; set;
        }


        /// <summary>
        /// Список типов значений, которые можно получить от исполнителя, если
        /// он может получать и отправлять серверу какие-либо данные (исполнять
        /// роль датчика)
        /// </summary>
        public List<AqValueType<dynamic>> Retrieves 
        { 
            get; set;
        }

        /// <summary>
        /// Список типов действий, которые исполнитель может выполнять, если он
        /// может получать от сервера команды и выполнять по ним какие-либо 
        /// действия
        /// </summary>
        /// <remarks>
        /// Поддерживаемые типы:
        /// <see cref="AqActionType{T}"/>, 
        /// <see cref="AqActionType{T1, T2}"/>,
        /// <see cref="AqActionType{T1, T2, T3}"/>,
        /// <see cref="AqActionType{T1, T2, T3, T4}"/>
        /// </remarks>
        public List<dynamic> Executes
        { 
            get; set;
        }

        /// <summary>
        /// Используется ли исполнитель в системе?
        /// </summary>
        public bool IsEnabled 
        {
            get; set;
        }

        /// <summary>
        /// Контролируется ли исполнитель сервером напрямую, или он 
        /// контролируется своим материнским исполнителем?
        /// </summary>
        public bool IsControllable 
        {
            get; set;
        }

        /// <summary>
        /// Способен ли исполнитель иметь других исполнителей в подчинении?
        /// </summary>
        public bool IsFertile 
        {
            get; set;
        }

        /// <summary>
        /// Индентификатор протокола
        /// </summary>
        public string Platform 
        {
            get;
        }

        /// <summary>
        /// Индентификатор исполнителя. Генерируется при его инициализации, пред-
        /// ставляет из себя строку длиной 4 символа, состоящую из символов лати-
        /// ницы и цифр от 0 до 9
        /// </summary>
        public string DeviceId
        {
            get;
        }

        /// <summary>
        /// Адрес (его форма зависит от типа исполнителя), на котором он 
        /// располагается
        /// </summary>
        public string DeviceAddress
        {
            get; set;
        }

        /// <summary>
        /// Индентификатор драйвера исполнителя, представляет из себя строку дли-
        /// ной 4 символа, состоящую из символов латиницы и цифр от 0 до 9. Задаётся
        /// в определении драйвера исполнителя
        /// </summary>
        public string DriverId
        {
            get;
        }

        /// <summary>
        /// Информация для отображения в вершителях
        /// </summary>
        public DeviceDisplayData DisplayData
        {
            get; set;
        }
    }
}

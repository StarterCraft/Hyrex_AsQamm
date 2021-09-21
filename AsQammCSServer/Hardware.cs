using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace AsQammServer
{
    /// <summary> 
    /// Класс `комплекса` - высокоуровневого объединения нескольких исполнителей. Пока не разработан.
    /// </summary>
    public class AqHardwareComplex
    {

    }


    /// <summary>
    /// Класс, представляющий любого `исполнителя` (или, упрощённо, `устройство`)
    /// — устройство, находящееся в подчинении сервера.
    /// </summary>
    /// Все классы поддерживаемых типов устройств-исполнителей являются потомками 
    /// этого класса. `Исполнители` и `устройства` есть одно и то же, если не 
    /// указано иное! `Устройства` могут иметь подчинённых себе других `устройств`, 
    /// если это предусмотрено типом устройства.Они могут быть объединены в `комплексы`
    /// для более глубокого взаимодействия друг с другом.
    ///
    ///Информация о них находится в hardware.asqd в виде JSON-списка по схеме ниже.
    ///Там хранятся базовые настройки устройства, а также информация обо всех под-
    ///чинённых ему устройствах и их настройках:
    ///
    /// Все классы поддерживаемых типов устройств-исполнителей являются потомками
    /// этого класса. `Исполнители` и `устройства` есть одно и то же, если не указано
    /// иное! `Устройства` могут иметь подчинённых себе других `устройств`, если это 
    /// предусмотрено типом устройства. Они могут быть объединены в `комплексы` для
    /// более глубокого взаимодействия друг с другом.
    /// 
    /// Информация о них находится в hardware.asqd в виде JSON-списка по схеме ниже.
    /// Там хранятся базовые настройки устройства, а также информация обо всех под-
    /// чинённых ему устройствах и их настройках:
    /// 
    /// [
    ///     /*Объект устройства, где:
    ///       a —— ID драйвера устройства (любой ID драйвера представляет из себя
    ///        строку длиной 4 символа, состоящую из символов латиницы и цифр
    ///        от 0 до 9);
    ///       b —— адрес (его форма зависит от типа исполнителя), на котором он
    ///        располагается;
    ///       c —— Настройки исполнителя в виде "имя параметра: значение";
    ///       d —— какой-либо определитель способа подключения к подчинённому ис-
    ///        полнителю (например, для Arduino-исполнителя — адрес пина, на
    ///        котором располагается подчинённый исполнитель);
    ///       e —— ID драйвера подчинённого исполнителя;
    ///       f —— Настройки подчинённого исполнителя в виде 
    ///        "имя параметра: значение"
    ///     */
    ///     
    ///     [a, b, {
    ///     c,
    ///     "children": {
    ///     //В параметре children хранится информация о подчинённых испол-
    ///     //нителях, привязанных к исполнителю, если они им поддержива-
    ///     //ются
    ///     d: [e, {
    ///     f
    ///     },
    ///     
    ///     //другие определения подчинённых исполнителей по той же схеме
    ///     }
    ///     }
    ///     ],
    ///     
    ///     //другие определения исполнителей по той же схеме
    /// ]
    public class AqHardwareDevice
    {
        public struct ClientDisplayData
        {
            public string TypeDisplayName;
            public string TypeDescription;

            /// <summary>
            /// Отображаемое имя конкретного исполнителя. Может быть пустым
            /// </summary>
            public string InstanceName;

            /// <summary>
            /// Описание конкретного исполнителя. Может быть пустым
            /// </summary>
            public string InstanceDescription;

            public ClientDisplayData(
                string typeDisplayName, string typeDescription,
                string instanceName, string instanceDescription)
            {
                TypeDisplayName = typeDisplayName;
                TypeDescription = typeDescription;

                InstanceName = instanceName;
                InstanceDescription = instanceDescription;
            }
        }

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


        public AqHardwareDevice Parent;

        private List<AqHardwareDevice> _Children;
        public List<AqHardwareDevice> Children 
        { 
            get 
            {
                if (!IsFertile)
                    throw new NotImplementedException("Этот исполнитель не может иметь других исполнителей в подчинении");
                return _Children;
            }

            set
            {
                _Children = value;
            }
        }

        public bool IsEnabled;
        public bool IsControllable;
        public bool IsFertile;
        public bool CanRetrieve;
        public bool CanExecute;

        public readonly string Platform;
        public readonly string DeviceId;
        public readonly string DeviceAddress;
        public static readonly string DriverId;

        /// <summary>
        /// Информация для отображения в вершителях
        /// </summary>
        public ClientDisplayData DisplayData;


        /// <summary>
        /// Инициализировать объект абстрактного исполнителя. Этот конструктор преимущественно
        /// используется в драйверах исполнителей.
        /// </summary>
        /// 
        /// <param name="isEnabled">Используется ли этот исполнитель в системе или нет.</param>
        /// <param name="platform">Индентификатор протокола</param>
        /// <param name="address">Адрес (его форма зависит от типа исполнителя), 
        /// на котором он располагается</param>
        /// <param name="parent">Если исполнитель является подчинённым, то — 
        /// объект материнского исполнителя</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        /// <param name="isFertile">Способен ли исполнитель иметь других исполнителей в подчинении</param>
        /// <param name="canRetrieve"></param>
        /// <param name="canExecute"></param>
        public AqHardwareDevice(
            bool isEnabled, string id, string platform, string address,
            AqHardwareDevice parent = null, ClientDisplayData displayData = default, 
            bool isFertile = false)
        {
            (Parent, IsEnabled, IsFertile) = (parent, isEnabled, isFertile);
            (Platform, DeviceId, DeviceAddress) = (platform, id, address);
            IsControllable = Parent is not null;
        }
    }


    public class AqHardwareValueType
    {

    }


    public class AqHardwareSystem
    {

    }
}

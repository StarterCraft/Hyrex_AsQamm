using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using AsQammServer;


namespace AsQammServer.Hardware
{
    /// <summary>
    /// Объект для отображения информации о устройстве в вершителях
    /// </summary>
    public class DeviceDisplayData: Client.AqAbstractDisplayData
    {
        public DeviceDisplayData(
            string typeDisplayName = "Unnamed Type",
            string typeDescription = "Unnamed Type",
            string instanceName = "Untitled",
            string instanceDescription = "No description")
        {
            TypeDisplayName = typeDisplayName;
            TypeDescription = typeDescription;
            InstanceName = instanceName;
            InstanceDescription = instanceDescription;
        }
    }


    public class DeviceDisabledException: Exception
    {
        public DeviceDisabledException(AqAbstractDevice device): 
            base($"Device {device.DeviceId} of type {device.GetType().Name} " +
                $"at {device.DeviceAddress} is disabled and unable to complete " +
                $"the requested operation.")
        {

        }
    }


    /// <summary>
    /// Класс, представляющий любого `исполнителя` (или, упрощённо, `устройство`)
    /// — устройство, находящееся в подчинении сервера.
    /// </summary>
    /// Все классы поддерживаемых типов устройств-исполнителей являются потомками 
    /// этого класса. `Исполнители` и `устройства` есть одно и то же, если не 
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
    public abstract class AqAbstractDevice
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
        /// Событие, вызываемое при изменении свойства 
        /// <see cref="IsEnabled"/> на <see langword="true"/> 
        /// (при активации исполнителя от системы).
        /// </summary>
        public event Action Activated;

        /// <summary>
        /// Событие, вызываемое при изменении свойства 
        /// <see cref="IsEnabled"/> на <see langword="false"/> 
        /// (при отклюбчении исполнителя от системы).
        /// </summary>
        public event Action Deactivated;


        /// <summary>
        /// Метод, вызываемый при изменении свойства 
        /// <see cref="IsEnabled"/> на <see langword="true"/> 
        /// (при активации исполнителя от системы).
        /// </summary>
        public abstract void OnActivation();

        /// <summary>
        /// Метод, вызываемый при изменении свойства 
        /// <see cref="IsEnabled"/> на <see langword="true"/> 
        /// (при отключении исполнителя от системы).
        /// </summary>
        public abstract void OnDeactivation();


        /// <summary>
        /// Если исполнитель является подчинённым, то в этом атрибуте будет нахо-
        /// диться ссылка на объект материнского объекта, иначе — null
        /// </summary>
        public AqAbstractDevice Parent
        {
            get; set;
        }

        /// <summary>
        /// Список подчинённых исполнителей этого исполнителя. Не инициализируется,
        /// если исполнитель не может иметь подчинённых исполнителей
        /// </summary>
        public List<AqAbstractDevice> Children
        {
            get
            {
                if (!IsFertile)
                    throw new NotImplementedException("Это устройство не может иметь подчинённых");

                else return _Children;
            }


            set
            {
                if (!IsFertile)
                    throw new NotImplementedException("Это устройство не может иметь подчинённых");

                else _Children = value;
            }
        }

        private List<AqAbstractDevice> _Children;

        public bool CanRetrieve;
        public bool CanExecute;


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
            get
            {
                return _IsEnabled;
            }

            
            set
            {
                if (_IsEnabled != value)
                {
                    if (value)
                    {
                        OnActivation();
                        _IsEnabled = true;
                        Activated();
                    }

                    else
                    {
                        OnDeactivation();
                        _IsEnabled = false;
                        Deactivated();
                    }
                }

                else return;
            }
        }

        /// <summary>
        /// Хранилище для свойства <see cref="IsEnabled"/>
        /// </summary>
        private bool _IsEnabled;

        /// <summary>
        /// Контролируется ли исполнитель сервером напрямую, или он 
        /// контролируется своим материнским исполнителем?
        /// </summary>
        public bool IsControllable;

        /// <summary>
        /// Способен ли исполнитель иметь других исполнителей в подчинении?
        /// </summary>
        public bool IsFertile;

        /// <summary>
        /// Индентификатор протокола
        /// </summary>
        public readonly string Platform;

        /// <summary>
        /// Индентификатор исполнителя. Генерируется при его инициализации, пред-
        /// ставляет из себя строку длиной 4 символа, состоящую из символов лати-
        /// ницы и цифр от 0 до 9
        /// </summary>
        public readonly string DeviceId;

        /// <summary>
        /// Адрес (его форма зависит от типа исполнителя), на котором он 
        /// располагается
        /// </summary>
        public readonly string DeviceAddress;

        /// <summary>
        /// Индентификатор драйвера исполнителя, представляет из себя строку дли-
        /// ной 4 символа, состоящую из символов латиницы и цифр от 0 до 9. Задаётся
        /// в определении драйвера исполнителя
        /// </summary>
        public readonly string DriverId;

        /// <summary>
        /// Информация для отображения в вершителях
        /// </summary>
        public DeviceDisplayData DisplayData;


        /// <summary>
        /// Конструктор для наследования.
        /// </summary>
        /// <remarks>
        /// <see cref="Parent"/> здесь нё задаётся, так как он может быть null
        /// </remarks>
        /// <param name="isEnabled">Используется ли исполнитель в системе?</param>
        /// <param name="platform">Индентификатор протокола</param>
        /// <param name="deviceId">Индентификатор исполнителя</param>
        /// <param name="deviceAddress">Адрес на котором располагается исполнитель</param>
        /// <param name="driverId">Индентификатор драйвера исполнителя</param>
        protected AqAbstractDevice(
            bool isEnabled,
            string platform,
            string deviceId,
            string deviceAddress,
            string driverId,
            DeviceDisplayData displayData)
        {
            IsEnabled = isEnabled;
            Platform = platform;
            DeviceId = deviceId;
            DeviceAddress = deviceAddress;
            DriverId = driverId;
            DisplayData = displayData;
        }
    }
}

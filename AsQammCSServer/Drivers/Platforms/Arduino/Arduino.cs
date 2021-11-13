using System;
using System.Collections.Generic;
using System.Linq;
using System.IO.Ports;
using System.Threading.Tasks;

using AsQammServer.Hardware;
using AsQammServer.Utilities;

using Solid.Arduino;
using Solid.Arduino.Firmata;


namespace AsQammServer.Drivers
{
    /// <summary>
    /// Класс Arduino-исполнителя. Имеет функциональность Firmata,
    /// функциональность приёма и отправки строковых сообщений ASCII,
    /// функциональность работы с модулями.
    /// </summary>
    public abstract class ArduinoDevice: AqAbstractDevice
    {
        /// <summary>
        /// Класс для работы со строковыми сообщениями-ответами от Arduino-
        /// исполнителя. Firmata посылает ответы на строковые команды в виде
        /// строк, кото- рые могут быть двух видов: бeз ошибки и с ошибкой.
        /// </summary>
        /// 
        /// Схема безошибочного строкового ответа от исполнителя:
        /// 'OK;{a};{b}', где:
        ///     a —— Имя метода, который вызывался и на который исполнитель
        ///          отправляет ответ;
        ///     b —— Результат выполнения метода.Может представлять из себя
        ///          число или строку.Если результат представляет собой спи-
        ///          сок, то каждый его элемент записывается через точку с
        ///          запятой.
        ///
        /// Схема строкового сообщения об ошибке(ответа) от исполнителя:
        /// 'ERR;{a};{b}', где:
        ///     a —— Имя метода, который вызывался и на который исполнитель
        ///          отправляет ответ;
        ///     b —— Код ошибки, зависит от вызываемого метода(для каждого
        ///          метода существуют свои коды ошибки, о них можно узнать
        ///          в документации к функциональным библиотекам AsQamm Arduino).
        public class FirmataStringMessage
        {
            /// <summary>
            /// Перечисление возможных видов строкового сообщения
            /// </summary>
            public enum MessageType
            {
                OK = 1,
                Error = 0,
                NotSpecified = -1
            }

            /// <summary>
            /// Исключение, которое вызывается, если сообщение, полученное от
            /// исполнителя, не соответствует синтаксису строковых сообщений.
            /// </summary>
            public class SyntaxError : Exception
            {
                public SyntaxError() :
                    base("От Arduino-исполнителя получено некорректное строковое сообщение")
                {

                }
            }

            /// <summary>
            /// Тип сообщения
            /// </summary>
            public readonly MessageType Type;

            /// <summary>
            /// Имя метода
            /// </summary>
            public readonly string MethodName;

            /// <summary>
            /// Код типа сообщения
            /// </summary>
            public readonly string StatusCode;

            /// <summary>
            /// Время получения сообщения
            /// </summary>
            public readonly DateTimeOffset ReceivedAt;

            /// <summary>
            /// Полезная нагрузка сообщения
            /// </summary>
            public readonly List<string> Received;

            /// <summary>
            ///  Инициализировать обработчик строкового сообщения. Если после-
            ///  днее не соответствует синтаксису строковых сообщений, будет
            ///  вызвано исключение <see cref="Synta"/>.
            /// </summary>
            /// <param name="raw">Строковое сообщение от Arduino-исполнителя в виде 
            /// строки.
            /// </param>
            public FirmataStringMessage(string raw)
            {
                List<string> components = raw.Split(';').ToList();

                if (components.Count < 2) throw new SyntaxError();

                StatusCode = components[0];
                MethodName = components[1];
                Received = new List<string>();
                ReceivedAt = DateTimeOffset.Now;

                switch (StatusCode)
                {
                    case "OK":
                        Type = MessageType.OK;
                        Received = components.GetRange(2, components.Count);
                        break;

                    case "ERR":
                        Type = MessageType.Error;
                        Received.Add(components[2]);
                        break;

                    default:
                        throw new SyntaxError();
                }
            }
        }

        /// <summary>
        /// Сессия подключения к Аrduino
        /// </summary>
        public ArduinoSession Session
        {
            get
            {
                return _Session ?? throw new DeviceDisabledException(this);
            }

            set
            {
                _Session = value;
            }
        }

        /// <summary>
        /// Xранилище для свойства <see cref="Session"/>
        /// </summary>
        private ArduinoSession _Session;


        private PinCapability[] Pins;

        /// <summary>
        /// Порт для подключения
        /// </summary>
        public string ComPort;

        /// <summary>
        /// Скорость подключения
        /// </summary>
        public SerialBaudRate BaudRate;

        /// <summary>
        /// Сообщения, полученные от устройства
        /// </summary>
        public List<FirmataStringMessage> ReceivedMessages;


        /// <summary>Инициализировать экземпляр базового класса Arduino-исполнителя.
        /// Такие исполнители работают на базе протокола Firmata, сервер использует
        /// библиотеку SolidSoils.Arduino для коммутации с ними.
        /// </summary>
        /// 
        /// <param name="isEnabled">Используется ли этот исполнитель в системе или нет.</param>
        /// <param name="comPort">COM-порт, на котором необходимо запустить службу Firmata 
        /// для этого исполнителя</param>
        /// <param name="driverId">Индентификатор драйвера исполнителя</param>
        /// <param name="baudRate">Скорость подключения к исполнителю, бод</param>
        /// <param name="parent">Если исполнитель является подчинённым, то — 
        /// объект материнского исполнителя</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public ArduinoDevice(
            bool isEnabled,
            string comPort,
            string driverId,

            SerialBaudRate baudRate = SerialBaudRate.Bps_115200,
            AqAbstractDevice parent = null,
            DeviceDisplayData displayData = default):

            base(isEnabled, parent is null, true,
                "Arduino", comPort, driverId, ConnectionType.WireFirmata,
                displayData)
        {
            ComPort = comPort;
            Parent = parent;
            BaudRate = baudRate;
        }


        /// <inheritdoc/>
        public override void OnActivation()
        {
            Session = new(new EnhancedSerialConnection(ComPort, BaudRate));
            Session.StringReceived += ParseString;
            Pins = Session.GetBoardCapabilityAsync().Result.Pins;
        }


        /// <inheritdoc/>
        public override void OnDeactivation()
        {
            Session?.Dispose();
            Session = null;
            Pins = null;
        }


        /// <inheritdoc/>
        public override string ToString()
        {
            return $"{DeviceId} type Arduboard ({DisplayData.TypeDisplayName}) at {ComPort}";
        }


        /// <summary>
        /// Обработать полученную от Arduino-исполнителя строку.
        /// Вызывается автоматически при получении строкового сообщения.
        /// </summary>
        private void ParseString(object sender, StringEventArgs eventArgs)
        {
            ReceivedMessages.AppendInPlace(new FirmataStringMessage(eventArgs.Text));
        }

        /// <summary>
        /// Получить последнее полученное от платы сообщение Firmata.
        /// </summary>
        /// <param name="messageType">Необходимый <see cref="FirmataStringMessage.MessageType">
        /// тип сообщения</see></param>
        /// <returns>Последнее полученное сообщение</returns>
        public FirmataStringMessage GetLastMessage(
            FirmataStringMessage.MessageType messageType = FirmataStringMessage.MessageType.NotSpecified)
        {
            DateTimeOffset currentTime = DateTimeOffset.Now;
            List<TimeSpan> timeSpans = new();

            if (messageType == FirmataStringMessage.MessageType.NotSpecified)
            {
                foreach (FirmataStringMessage message in ReceivedMessages)
                    timeSpans.AppendInPlace(currentTime - message.ReceivedAt);
            }

            else
            {
                foreach (FirmataStringMessage message in ReceivedMessages)
                    if (message.Type == messageType) timeSpans.AppendInPlace(currentTime - message.ReceivedAt);
            }

            return ReceivedMessages.Single(message => (currentTime - message.ReceivedAt) == timeSpans.Min());
        }
    }


    /// <summary>
    /// Класс Аrduino-датчика, являющегося исполнителем. 
    /// Они имеют два подтипа: <see cref="SensorType.Analog"/> (для аналоговых) и
    /// <see cref="SensorType.Digital"/> (для цифровых датчиков).
    /// </summary>
    public abstract class ArduinoSensor : AqAbstractDevice
    {
        /// <summary>
        /// Перечисление возможных подтипов Arduino-датчиков
        /// </summary>
        public enum SensorType
        {
            Analog = 0,
            Digital = 1
        }


        /// <summary>
        /// Подтип датчика
        /// </summary>
        public readonly SensorType Type;


        /// <summary>
        /// Инициализировать Аrduino-датчик.
        /// </summary>
        /// <param name="isEnabled">
        /// Использовать ли этот датчик или нет. Если этот параметр
        /// отключить, то регистрация его значений системой статистики
        /// не будет выполняться, а также частично или полностью перес-
        /// танут работать правила, в условиях которых фигурирует данный
        /// датчик.
        /// </param>
        /// <param name="atPin">Адрес пина Arduino-исполнителя, к которому подключён датчик</param>
        /// <param name="deviceId">Индентификатор исполнителя</param>
        /// <param name="driverId">Индентификатор драйвера исполнителя</param>
        /// <param name="type">Подтип датчика</param>
        /// <param name="parent">Объект Arduino-исполнителя, к которому подключён датчик</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public ArduinoSensor(
            bool isEnabled,
            string atPin,
            string driverId,
            ArduinoDevice parent,
            SensorType type,
            DeviceDisplayData displayData = default) :

            base(isEnabled, false, false, "Arduino", $"{parent.DeviceAddress}:{atPin}", 
                driverId, ConnectionType.WireGeneric, displayData)
        {
            Type = type;
        }
    }


    /// <summary>
    /// Класс подчинённых исполнителей, работающих на вывод, для Arduino-
    /// исполнителя (например, сервопривод). Они имеют два подтипа: 
    /// <see cref="ExecutorType.Analog"/> (для аналоговых) и 
    /// <see cref="ExecutorType.Digital"/> (для цифровых устройств исполнения).
    /// </summary>
    public abstract class ArduinoExecutor : AqAbstractDevice
    {
        /// <summary>
        /// Перечисление возможных подвидов подчинённых
        /// Arduino-исполнителей, работающих на вывод
        /// </summary>
        public enum ExecutorType
        {
            Analog = 0,
            Digital = 1
        }


        /// <summary>
        /// Подвид подчинённого исполнителя
        /// </summary>
        public readonly ExecutorType Type;


        /// <summary>
        /// Инициализировать Аrduino-датчик.
        /// </summary>
        /// <param name="isEnabled">
        /// Использовать ли этого исполнителя или нет. Если этот 
        /// параметр отключить, то на исполнителя невозможно будет отдавать
        /// какие-либо команды, а также частично или полностью перестанут
        /// работать правила, в действиях которых фигурирует данный исполнитель.
        /// </param>
        /// <param name="atPin">Адрес пина Arduino-исполнителя, к которому подключён подчинённый</param>
        /// <param name="deviceId">Индентификатор исполнителя</param>
        /// <param name="driverId">Индентификатор драйвера исполнителя</param>
        /// <param name="type">Подтип датчика</param>
        /// <param name="parent">Объект Arduino-исполнителя, к которому подключён подчинённый</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public ArduinoExecutor(
            string atPin,
            bool isEnabled,
            string driverId,
            ExecutorType type,
            ArduinoDevice parent,
            DeviceDisplayData displayData = default) :

            base(isEnabled, false, false, "Arduino", $"{parent.DeviceAddress}:{atPin}",
                driverId, ConnectionType.WireGeneric, displayData)
        {
            IsFertile = false;
            Type = type;
        }
    }
}

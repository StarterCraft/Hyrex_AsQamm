using System;

using AsQammServer.Client;


namespace AsQammServer.Hardware
{
    public class ValueTypeDisplayData: AqAbstractDisplayData
    {
        public ValueTypeDisplayData(
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


    /// <summary>
    /// Класс типа значений, получаемых от объекта с ролью Retriever.
    /// </summary>
    public class AqValueType<T>
    {
        public AqAbstractDevice Parent;
        public string Id;
        public string Unit;
        public Func<T> Get;

        public float ProbeFrequency;
        private bool IsCalibrateable;
        public Action<T> Calibrate;

        private T _CalibrationValue;
        public T CalibrationValue 
        {
            get 
            {
                if (!IsCalibrateable)
                    throw new NotSupportedException("Это значение не допускает калибровки");

                return _CalibrationValue;
            }

            
            set
            {
                if (!IsCalibrateable)
                    throw new NotSupportedException("Это значение не допускает калибровки");

                _CalibrationValue = value;
            }
        }

        public ValueTypeDisplayData DisplayData;


        /// <summary>
        /// Конструктор типа значений, получаемых от исполнителя с ролью Retriever.
        /// </summary>
        /// <param name="parent"><see cref="IAqDevice">Исполнитель</see>, 
        /// который умеет передавать этот тип значений</param>
        /// <param name="id">Строковый индентификатор типа значения</param>
        /// <param name="getter">Метод получения значения</param>
        /// <param name="frequency">Частота опроса этого значения</param>
        /// <param name="calm">Метод калибровки исполнителя для этого типа
        /// значения</param>
        /// <param name="calv">Значение калибровки исполнителя для этого типа
        /// его значения</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public AqValueType(
            AqAbstractDevice parent,
            string id,
            string unit,
            Func<T> getter,
            float frequency,
            Action<T> calm = null,
            T calv = default,
            ValueTypeDisplayData displayData = default)
        {
            (Parent, Id, Unit) = (parent, id, unit);
            (Get, ProbeFrequency) = (getter, frequency);
            (Calibrate, IsCalibrateable, CalibrationValue) = (calm, calm is null, calv);
            DisplayData = displayData;
        }
    }
}

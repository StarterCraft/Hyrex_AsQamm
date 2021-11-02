using System;

using AsQammServer.Client;


namespace AsQammServer.Hardware
{
    public class ActionTypeDisplayData: AqDisplayData
    {
        public ActionTypeDisplayData(
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
    /// Класс типа действия, которое может выполнить исполнитель с ролью Executor.
    /// </summary>
    public class AqActionType
    {
        public IAqDevice Parent;
        public string Id;
        public Action Run;

        public ActionTypeDisplayData DisplayData;


        /// <summary>
        /// Конструктор типа действия, которое может выполнить исполнитель с ролью Executor.
        /// </summary>
        /// <param name="parent">Исполнитель, который умеет выполнять этот тип действий</param>
        /// <param name="run">Метод выполнения действия</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public AqActionType(
            IAqDevice parent,
            Action run,
            ActionTypeDisplayData displayData)
        {
            Parent = parent;
            Run = run;
            DisplayData = displayData;
        }
    }




    /// <summary>
    /// Класс типа действия, которое может выполнить исполнитель с ролью Executor.
    /// </summary>
    public class AqActionType<T>
    {
        public IAqDevice Parent;
        public string Id;
        public Action<T> Run;

        public ActionTypeDisplayData DisplayData;


        /// <summary>
        /// Конструктор типа действия, которое может выполнить исполнитель с ролью Executor.
        /// </summary>
        /// <param name="parent">Исполнитель, который умеет выполнять этот тип действий</param>
        /// <param name="run">Метод выполнения действия</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public AqActionType(
            IAqDevice parent,
            Action<T> run,
            ActionTypeDisplayData displayData
            )
        {
            Parent = parent;
            Run = run;
            DisplayData = displayData;
        }
    }


    /// <summary>
    /// Класс типа действия, которое может выполнить исполнитель с ролью Executor.
    /// </summary>
    public class AqActionType<T1, T2>
    {
        public IAqDevice Parent;
        public string Id;
        public Action<T1, T2> Run;

        public ActionTypeDisplayData DisplayData;


        /// <summary>
        /// Конструктор типа действия, которое может выполнить исполнитель с ролью Executor.
        /// </summary>
        /// <param name="parent">Исполнитель, который умеет выполнять этот тип действий</param>
        /// <param name="run">Метод выполнения действия</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public AqActionType(
            IAqDevice parent,
            Action<T1, T2> run,
            ActionTypeDisplayData displayData
            )
        {
            Parent = parent;
            Run = run;
            DisplayData = displayData;
        }
    }


    /// <summary>
    /// Класс типа действия, которое может выполнить исполнитель с ролью Executor.
    /// </summary>
    public class AqActionType<T1, T2, T3>
    {
        public IAqDevice Parent;
        public string Id;
        public Action<T1, T2, T3> Run;

        public ActionTypeDisplayData DisplayData;


        /// <summary>
        /// Конструктор типа действия, которое может выполнить исполнитель с ролью Executor.
        /// </summary>
        /// <param name="parent">Исполнитель, который умеет выполнять этот тип действий</param>
        /// <param name="run">Метод выполнения действия</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public AqActionType(
            IAqDevice parent,
            Action<T1, T2, T3> run,
            ActionTypeDisplayData displayData
            )
        {
            Parent = parent;
            Run = run;
            DisplayData = displayData;
        }
    }


    /// <summary>
    /// Класс типа действия, которое может выполнить исполнитель с ролью Executor.
    /// </summary>
    public class AqActionType<T1, T2, T3, T4>
    {
        public IAqDevice Parent;
        public string Id;
        public Action<T1, T2, T3, T4> Run;

        public ActionTypeDisplayData DisplayData;


        /// <summary>
        /// Конструктор типа действия, которое может выполнить исполнитель с ролью Executor.
        /// </summary>
        /// <param name="parent">Исполнитель, который умеет выполнять этот тип действий</param>
        /// <param name="run">Метод выполнения действия</param>
        /// <param name="displayData">Информация для отображения в вершителях</param>
        public AqActionType(
            IAqDevice parent,
            Action<T1, T2, T3, T4> run,
            ActionTypeDisplayData displayData
            )
        {
            Parent = parent;
            Run = run;
            DisplayData = displayData;
        }
    }
}

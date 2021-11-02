using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

using AsQammServer;


namespace AsQammServer.RuntimeLogic
{
    /// <summary>
    /// Правило, являющееся совокупностью триггера <see cref="AqRuleTrigger"/>
    /// и действий <see cref="AqRuleAction"/>, которое выполняет действия по 
    /// порядку, когда условие триггера становится истинным.
    /// </summary>
    public class AqRule
    {
        /// <summary>
        /// Триггер, при истинности условия которого выполняются
        /// <see cref="Actions">действия</see>.
        /// </summary>
        public AqRuleTrigger Trigger;

        /// <summary>
        /// Действия, которые выполняются по порядку, когда условие
        /// <see cref="Trigger">триггера</see> становится истинным.
        /// </summary>
        public LinkedList<AqRuleAction> Actions;
    }


    /// <summary>
    /// 
    /// </summary>
    public class AqRuleTrigger
    {
        public event Action Activated;


    }


    /// <summary>
    /// 
    /// </summary>
    public class AqRuleAction
    {

    }
}

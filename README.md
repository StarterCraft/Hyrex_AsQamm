# Hyrex AsQamm

### RU-CY
Проект системы Умного дома на базе
Python,
Qt5,
Arduino, 
Firmata

Основная структура системы:
- **Средства управления**, или ***вершители*** — *позволяют зарегистрированным в системе пользователям отдавать немедленные команды управляющему серверу, менять правила его работы и просматривать данные, полученные с него. Высшая ипостась проекта;*
- **Управляющий сервер**, или ***обработчик*** — *ПО, устанавливоемое на ПК. Хранит информацию о зарегистрированных в системе пользoвателях, а также — обо всех без исключения компонентах системы. Отправляет немедленные команды на подключённых к нему **исполнителей**, отправляет им команды также в соответствии с правилами, заданными ему, а также получает и сохраняет данные, полученные с датчиков на **исполнителях** и сохраняет их для последующего просмотра через **вершитель**;*
- **Устройства исполнения**, или ***исполнители*** *получают команды для выполнения от **обработчика** и передают ему данные с датчиков. К примеру, могут являться Arduino-устройствами, установленными, например, в теплице. Имеют подключённые датчики и средства исполнения команд (сервоприводы, реле и т. д.), которые называются **модулями**. Также в будущем планируется добавить поддержку устройств, не имеющих отношения к Arduino;*
- **Комплексы** — *объединения **устройств исполнения**. Нужны для глубокой синхронизации работы нескольких таких устройств друг с другом. Например, теплица — **комплекс**;*
- **Модули** — *устройства ввода-вывода (разные датчики и средства исполнения команд), подключенные к **Arduino**-исполнителям, такие как датчики как устройства ввода и сервопририводы как устройства вывода.* 


Определение некоторых терминов:
- **Немедленные команды** — *это команды, которые сервер получает от **обработчика** по велению пользователя, если таковому нужно заставить **обработчик** сделать что-то немедленно. Например, если вы хотите, чтобы сервер запустил уборку прямо сейчас, вы отправляете серверу **немедленную команду** через **вершителя**, и он немедленно начинает уборку. Команды перекрывают правила до тех пор, пока пользователь не попросит сервер вернуться к работе по правилам*;
- **Правила работы сервера** — *запрограммированные сценарии, по которым работает сервер. Например,* `если температура в теплице опустилась ниже 15 градусов, включить отопление` — *это **правило**. Оно может быть перекрыто, если это нужно пользователю. Например, Ваши датчики температуры неисправны, а отопление нужно включить прямо сейчас: в такой ситуации вы направите серверу **немедленную команду**, и он тут же включит отопление. Сервер вернётся к работе по правилам, когда вы попросите его об этом*.


Системой Hyrex AsQamm можно управлять из трёх компонентов:
- Приложение управления системой и просмотра данных для Windows;
- Приложение управления системой и просмотра данных для Android (добавляется опционально по желанию пользователя);
- Интерактивный экран (планируется).


### RU-GL
Ⱂⱃⱁⰵⰽⱅ ⱄⰻⱄⱅⰵⰿⱏⰹ Ⱆⰿⱀⱁⰳⱁ ⰴⱁⰿⰰ ⱀⰰ ⰱⰰⰸⰵ:
Python,
Qt5,
Arduino,
Firmata


Ⱁⱄⱀⱁⰲⱀⰰⱑ ⱄⱅⱃⱆⰽⱅⱆⱃⰰ ⱄⰻⱄⱅⰵⰿⱏⰹ:
- **Ⱄⱃⰵⰴⱄⱅⰲⰰ ⱆⱀⱃⰰⰲⰾⰵⱀⰻⱑ**, ⰻⰾⰻ ***ⰲⰵⱃⱎⰻⱅⰵⰾⰻ*** — *ⱀⱁⰸⰲⱁⰾⱑⱓⱅ ⰸⰰⱃⰵⰳⰻⱄⱅⱃⰻⱃⱁⰲⰰⱀⱀⱏⰹⰿ ⰲ ⱄⰻⱄⱅⰵⰿⰵ ⱀⱁⰾⱜⰸⱁⰲⰰⱅⰵⰾⱑⰿ ⱁⱅⰴⰰⰲⰰⱅⱜ ⱀⰵⰿⰵⰴⰾⰵⱀⱀⱏⰹⰵ ⰽⱁⰿⰰⱀⰴⱏⰹ ⱆⱀⱃⰰⰲⰾⱑⱓⱋⰵⰿⱆ ⱄⰵⱃⰲⰵⱃⱆ, ⰿⰵⱀⱑⱅⱜ ⱀⱃⰰⰲⰻⰾⰰ ⰵⰳⱁ ⱃⰰⰱⱁⱅⱏⰹ ⰻ ⱀⱃⱁⱄⰿⰰⱅⱃⰻⰲⰰⱅⱜ ⰴⰰⱀⱀⱏⰹⰵ, ⱀⱁⰾⱆⱍⰵⱀⱀⱏⰹⰵ ⱄ ⱀⰵⰳⱁ. Ⰲⱏⰹⱄⱎⰰⱑ ⰻⱀⱁⱄⱅⰰⱄⱜ ⱀⱃⱁⰵⰽⱅⱃⰰ;*
- **Ⱆⱀⱃⰰⰲⰾⱑⱓⱋⰻⰺ ⱄⰵⱃⰲⰵⱃ**, ⰻⰾⰻ ***ⱁⰱⱃⰰⰱⱁⱅⱍⰻⰽ*** — *ⰒⰑ, ⱆⱄⱅⰰⱀⰰⰲⰾⰻⰲⰰⰵⰿⱁⰵ ⱀⰰ ⰒⰍ. Ⱈⱃⰰⱀⰻⱅ ⰻⱀⱇⱁⱃⰿⰰⱌⰻⱓ ⱁ ⰸⰰⱃⰵⰳⰻⱄⱅⱃⰻⱃⱁⰲⰰⱀⱀⱏⰹⱈ ⰲ ⱄⰻⱄⱅⰵⰿⰵ ⱀⱁⰾⱜⰸⱁⰲⰰⱅⰵⰾⱑⱈ, ⰰ ⱅⰰⰽⰶⰵ — ⱁⰱⱁ ⰲⱄⰵⱈ ⰱⰵⰸ ⰻⱄⰽⰾⱓⱍⰵⱀⰻⱑ ⰽⱁⰿⱀⱁⱀⰵⱀⱅⰰⱈ ⱄⰻⱄⱅⰵⰿⱏⰹ. Ⱁⱅⱀⱃⰰⰲⰾⱑⰵⱅ ⱀⰵⰿⰵⰴⰾⰵⱀⱀⱏⰹⰵ ⰽⱁⰿⰰⱀⰴⱏⰹ ⱀⰰ ⱀⱁⰴⰽⰾⱓⱍⱖⱀⱀⱏⰹⱈ ⰽ ⱀⰵⰿⱆ **ⰻⱄⱀⱁⰾⱀⰻⱅⰵⰾⰵⰺ**, ⱁⱅⱀⱃⰰⰲⰾⱑⰵⱅ ⰻⰿ ⰽⱁⰿⰰⱀⰴⱏⰹ ⱅⰰⰽⰶⰵ ⰲ ⱄⱁⱁⱅⰲⰵⱅⱄⱅⰲⰻⰻ ⱄ ⱀⱃⰰⰲⰻⰾⰰⰿⰻ, ⰸⰰⰴⰰⱀⱀⱏⰹⰿⰻ ⰵⰿⱆ, ⰰ ⱅⰰⰽⰶⰵ ⱀⱁⰾⱆⱍⰰⰵⱅ ⰻ ⱄⱁⱈⱃⰰⱀⱑⰵⱅ ⰴⰰⱀⱀⱏⰹⰵ, ⱀⱁⰾⱆⱍⰵⱀⱀⱏⰹⰵ ⱄ ⰴⰰⱅⱍⰻⰽⱁⰲ ⱀⰰ **ⰻⱄⱀⱁⰾⱀⰻⱅⰵⰾⱑⱈ** ⰴⰾⱑ ⰻⱈ ⱀⱁⱄⰾⰵⰴⱆⱓⱋⰵⰳⱁ ⱀⱃⱁⱄⰿⱁⱅⱃⰰ ⱍⰵⱃⰵⰸ ***ⰲⰵⱃⱎⰻⱅⰵⰾⱜ***;*
- **Ⱆⱄⱅⱃⱁⰺⱄⱅⰲⰰ ⰻⱄⱀⱁⰾⱀⰵⱀⰻⱑ**, ⰻⰾⰻ ***ⰻⱄⱀⱁⰾⱀⰻⱅⰵⰾⰻ*** — *ⱀⱁⰾⱆⱍⰰⱓⱅ ⰽⱁⰿⰰⱀⰴⱏⰹ ⰴⰾⱑ ⰲⱏⰹⱀⱁⰾⱀⰵⱀⰻⱑ ⱁⱅ **ⱁⰱⱃⰰⰱⱁⱅⱍⰻⰽⰰ** ⰻ ⱀⱁⱃⰵⰴⰰⱓⱅ ⰵⰿⱆ ⰴⰰⱀⱀⱏⰹⰵ ⱄ ⱆⱄⱅⰰⱀⱁⰲⰾⰵⱀⱀⱏⰹⱈ ⱀⰰ ⱀⰻⱈ ⰴⰰⱅⱍⰻⰽⱁⰲ. Ⰽ ⱀⱃⰻⰿⰵⱃⱆ, ⰿⱁⰳⱆⱅ ⱑⰲⰾⱑⱅⱜⱄⱑ Arduino-ⱆⱄⱅⱃⱁⰺⱄⱅⰲⰰⰿⰻ, ⱆⱄⱅⰰⱀⱁⰲⰾⰵⱀⱀⱏⰹⰿⰻ, ⰽ ⱀⱃⰻⰿⰵⱃⱆ, ⰲ ⱅⰵⱀⰾⰻⱌⰵ. Ⰻⰿⰵⱓⱅ ⱀⱁⰴⰽⰾⱓⱍⰵⱀⱀⱏⰹⰵ **ⰿⱁⰴⱆⰾⰻ** — ⰴⰰⱅⱍⰻⰽⰻ ⰻ ⱄⱃⰵⰴⱄⱅⰲⰰ ⰻⱄⱀⱁⰾⱀⰵⱀⰻⱑ ⰽⱁⰿⰰⱀⰴ (ⱄⰵⱃⰲⱁⱀⱃⰻⰲⱁⰴⱏⰹ, ⱃⰵⰾⰵ ⰻ ⱅ. ⱀ.);*
- **Ⰽⱁⰿⱀⰾⰵⰽⱄⱏⰹ** — *ⱁⰱⱐⰵⰴⰻⱀⰵⱀⰻⱑ **ⱆⱄⱅⱃⱁⰺⱄⱅⰲ ⰻⱄⱀⱁⰾⱀⰵⱀⰻⱑ**. Ⱀⱆⰶⱀⱏⰹ ⰴⰾⱑ ⰳⰾⱆⰱⱁⰽⱁⰺ ⱄⰻⱀⱈⱃⱁⱀⰻⱑⰸⰰⱌⰻⰻ ⱃⰰⰱⱁⱅⱏⰹ ⱀⰵⱄⰽⱁⰾⱜⰽⰻⱈ ⱅⰰⰽⰻⱈ ⱆⱄⱅⱃⱁⰺⱄⱅⰲ ⰴⱃⱆⰳ ⱄ ⰴⱃⱆⰳⱁⰿ. Ⱀⰰⱀⱃⰻⰿⰵⱃ, ⱅⰵⱀⰾⰻⱌⰰ — ***ⰽⱁⰿⱀⰾⰵⰽⱄ***;*
- **Ⰿⱁⰴⱆⰾⰻ** — *ⱆⱄⱅⱃⱁⰺⱄⱅⰲⰰ ⰲⰲⱁⰴⰰ-ⰲⱏⰹⰲⱁⰴⰰ, ⱀⱁⰽⰾⱓⱍⰵⱀⱀⱏⰹⰵ ⰽ **Arduino**-ⰻⱄⱀⱁⰾⱀⰻⱅⰵⰾⱑⰿ, ⱅⰰⰽⰻⰵ ⰽⰰⰽ: ⰴⰰⱅⱍⰻⰽⰻ ⰽⰰⰽ ⱆⱄⱅⱃⱁⰺⱄⱅⰲⰰ ⰲⰲⱁⰴⰰ ⰻ ⱄⰵⱃⰲⱁⱀⱃⰻⰲⱁⰴⱏⰹ ⰽⰰⰽ ⱆⱄⱅⱃⱁⰺⱄⱅⰲⰰ ⰲⱏⰹⰲⱁⰴⰰ.*


Ⱁⰱⱐⱑⱄⱀⰵⱀⰻⰵ ⱀⰵⰽⱁⱅⱁⱃⱏⰹⱈ ⱅⰵⱃⰿⰻⱀⱁⰲ:
- **Ⱀⰵⰿⰵⰴⰾⰵⱀⱀⱏⰹⰵ ⰽⱁⰿⰰⱀⰴⱏⰹ** — *ⱏⰵⱅⱁ ⰽⱁⰿⰰⱀⰴⱏⰹ, ⰽⱁⱅⱁⱃⱏⰹⰵ ⱄⰵⱃⰲⰵⱃ ⱀⱁⰾⱆⱍⰰⰵⱅ ⱁⱅ **ⰲⰵⱃⱎⰻⱅⰵⰾⰵⰺ** ⱀⱁ ⰲⰵⰾⰵⱀⰻⱓ ⱀⱁⰾⱜⰸⱁⰲⰰⱅⰵⰾⱑ, ⰵⱄⰾⰻ ⱅⰰⰽⱁⰲⱁⰿⱆ ⱀⱆⰶⱀⱁ ⰸⰰⱄⱅⰰⰲⰻⱅⱜ **ⱁⰱⱃⰰⰱⱁⱅⱍⰻⰽ** ⱄⰴⰵⰾⰰⱅⱜ ⱍⱅⱁ-ⱅⱁ ⱀⰵⰿⰵⰴⰾⰵⱀⱀⱁ. Ⱀⰰⱀⱃⰻⰿⰵⱃ, ⰵⱄⰾⰻ Ⰲⱏⰹ ⱈⱁⱅⰻⱅⰵ, ⱍⱅⱁⰱⱏⰹ ⱄⰵⱃⰲⰵⱃ ⰸⰰⱀⱆⱄⱅⰻⰾ ⱆⰱⱁⱃⰽⱆ ⱀⱃⱑⰿⱁ ⱄⰵⰺⱍⰰⱄ, ⰲⱏⰹ ⱁⱅⱀⱃⰰⰲⰴⱑⰵⱅⰵ ⱄⰵⱃⰲⰵⱃⱆ **ⱀⰵⰿⰵⰴⰾⰵⱀⱀⱆⱓ ⰽⱁⰿⰰⱀⰴⱆ** ⱍⰵⱃⰵⰸ **ⰲⰵⱃⱎⰻⱅⰵⰾⱑ**, ⰻ ⱆⰱⱁⱃⰽⰰ ⰱⱆⰴⰵⱅ ⱀⰰⱍⰰⱅⰰ ⱄⱃⰰⰸⱆ ⰶⰵ. Ⰽⱁⰿⰰⱀⰴⱏⰹ ⱀⰵⱃⰵⰽⱃⱏⰹⰲⰰⱓⱅ **ⱀⱃⰰⰲⰻⰾⰰ ⱃⰰⰱⱁⱅⱏⰹ ⱄⰵⱃⰲⰵⱃⰰ** ⰴⱁ ⱅⰵⱈ ⱀⱁⱃ, ⱀⱁⰽⰰ ⱀⱁⰾⱜⰸⱁⰲⰰⱅⰵⰾⱜ ⱀⰵ ⱀⱁⱀⱃⱁⱄⱅⰻ ⱄⰵⱃⰲⰵⱃ ⰲⰵⱃⱀⱆⱅⱜⱄⱑ ⰽ ⱃⰰⰱⱁⱅⰵ ⱀⱁ ⱀⱃⰰⰲⰻⰾⰰⰿ*;
- **Ⱂⱃⰰⰲⰻⰾⰰ ⱃⰰⰱⱁⱅⱏⰹ ⱄⰵⱃⰲⰵⱃⰰ** — *ⰸⰰⱀⱃⱁⰳⱃⰰⰿⰿⰻⱃⱁⰲⰰⱀⱀⱏⰹⰵ ⱄⱌⰵⱀⰰⱃⰻⰻ, ⱀⱁ ⰽⱁⱅⱁⱃⱏⰹⰿ ⱃⰰⰱⱁⱅⰰⰵⱅ ⱄⰵⱃⰲⰵⱃ. Ⱀⰰⱀⱃⰻⰿⰵⱃ,* `ⰵⱄⰾⰻ ⱅⰵⰿⱀⰵⱃⰰⱅⱆⱃⰰ ⰲ ⱅⰵⱀⰾⰻⱌⰵ ⱁⱀⱆⱄⱅⰻⰾⰰⱄⱜ ⱀⰻⰶⰵ, ⱍⰵⰿ 15 ⰳⱃⰰⰴⱆⱄⱁⰲ, ⰲⰽⰾⱓⱍⰻⱅⱜ ⱁⱅⱁⱀⰾⰵⱀⰻⰵ` — *ⱏⰵⱅⱁ **ⱀⱃⰰⰲⰻⰾⱁ**. Ⱁⱀⱁ ⰿⱁⰶⰵⱅ ⰱⱏⰹⱅⱜ ⱀⰵⱃⰵⰽⱃⱏⰹⱅⱁ, ⰵⱄⰾⰻ ⱏⰵⱅⱁ ⱀⰵⱁⰱⱈⱁⰴⰻⰿⱁ ⱀⱁⰾⱜⰸⱁⰲⰰⱅⰵⰴⱓ. Ⱀⰰⱀⰻⰿⰵⱃ, Ⰲⰰⱎⰻ ⰴⰰⱅⱍⰻⰽⰻ ⱅⰵⰿⱀⰵⱃⰰⱅⱆⱃⱏⰹ ⱀⰵⰻⱄⱀⱃⰰⰲⱀⱏⰹ, ⰰ ⱁⱅⱁⱀⰾⰵⱀⰻⰵ ⱀⱆⰶⱀⱁ ⰲⰽⰾⱓⱍⰻⱅⱜ ⱁⱅⱁⱀⰾⰵⱀⰻⰵ ⱀⱃⱑⰿⱁ ⱄⰵⰺⱍⰰⱄ. Ⰲ ⱅⰰⰽⱁⰺ ⱄⰻⱅⱆⰰⱌⰻⰻ ⰲⱏⰹ ⱁⱅⱀⱃⰰⰲⰾⱑⰵⱅⰵ ⱄⰵⱃⰲⰵⱃⱆ **ⱀⰵⰿⰵⰴⰾⰵⱀⱀⱆⱓ ⰽⱁⰿⰰⱀⰴⱆ** ⱍⰵⱃⰵⰸ **ⰲⰵⱃⱎⰻⱅⰵⰾⱑ**, ⰻ ⱁⱅⱁⱀⰾⰵⱀⰻⰵ ⰱⱆⰴⰵⱅ ⰲⰽⰾⱓⱍⰵⱀⱁ. Ⱄⰵⱃⰲⰵⱃ ⰲⰵⱃⱀⱖⱅⱄⱑ ⰽ ⱃⰰⰱⱁⱅⰵ ⱀⱃ ⱀⱃⰰⰲⰻⰾⰰⰿ, ⰽⱁⰳⰴⰰ ⰲⱏⰹ ⱀⱁⱀⱃⱁⱄⰻⱅⰵ ⰵⰳⱁ ⱁⰱ ⱏⰵⱅⱁⰿ*.


Ⱄⰻⱄⱅⰵⰿⱁⰺ Hyrex AsQamm ⰿⱁⰶⱀⱁ ⱆⱀⱃⰰⰲⰾⱑⱅⱜ ⰻⰸ ⱅⱃⱖⱈ ⰽⱁⰿⱀⱁⱀⰵⱀⱅⱁⰲ:
- Ⱂⱃⰻⰾⱁⰶⰵⱀⰻⰵ ⱆⱀⱃⰰⰲⰾⰵⱀⰻⱑ ⱄⰻⱄⱅⰵⰿⱁⰺ ⰻ ⱀⱃⱁⱄⰿⱁⱅⱃⰰ ⰴⰰⱀⱀⱏⰹⱈ ⰴⰾⱑ Windows;
- Ⱂⱃⰻⰾⱁⰶⰵⱀⰻⰵ ⱆⱀⱃⰰⰲⰾⰵⱀⰻⱑ ⱄⰻⱄⱅⰵⰿⱁⰺ ⰻ ⱀⱃⱁⱄⰿⱁⱅⱃⰰ ⰴⰰⱀⱀⱏⰹⱈ ⰴⰾⱑ Android (ⰴⱁⰱⰰⰲⰾⱑⰵⱅⱄⱑ ⱁⱀⱌⰻⱁⱀⰰⰾⱜⱀⱁ ⱀⱁ ⰶⰵⰾⰰⱀⰻⱓ ⱀⱁⰾⱜⰸⱁⰲⰰⱅⰵⰾⱑ);
- Ⰻⱀⱅⰵⱃⰰⰽⱅⰻⰲⱀⱏⰹⰺ ⱏⰵⰽⱃⰰⱀ (ⱀⰾⰰⱀⰻⱃⱆⰵⱅⱄⱑ).


### EN-INT
An smart (intelligent) house system project based on
Python,
Qt5,
Arduino,
Firmata

General description of the system's structure:
- **Management software**, or ***rulers*** *are letting registered users to give instant-done instructions to the controlling server, to manage its working rules and to review the datareceived from the server. The highest hypostasis of the system and the project*;
- **Controlling server**, or the ***processor*** (aka the ***server***) *is a software being installed on a PC which works in unstopping mode (as a server). It stores registered users' information, and the information about every and all system's components. It sends commands to the **executors** according to **rules**, if a user wants to execute an immediate command, the **server** sends them to **executors** too. The **server** also receives data from the **executors**' sensors, stores and formats it for being reviewable via a **ruler***;
- **Executing devices**, or ***executors*** *are receiving commands from the **server**, and they send their installed sensors' data. For example, they can be presented as an Arduino device installed in your greenhouse. They can have **modules** connected to them*;
- **Complexes** *are high-level interaction unions of **executors**. They are neseccary to deeply synchronize the devices installed in one explicit zone with each other. Fro exaple, a greenhouse is a **complex***;
- **Modules** *is a termine for the I/O devices (various sensors and output devices) connected to the Arduino=**executors**, like temperature sensors as input devices and servo motors as output devices.*

Some termins' description:
- **Immediate commands** *are commands, which the server can receive if a **ruler**'s user will want to do something to the system immediately. For example, if you want the server to start cleaning procedures right now, you send an **immediate command** to the server and it starts the cleaning immediately. The commands can override rules untill the user asks the server to start working normally*;
- **Server's working rules** *are programmed scenarios, which the server follows in its everyday work. For example,* `if the temperature in the greenhouse is lower than 15 degrees, turn on the heating systems` *is a **rule**. It can be overriden by the user, if he wants to. For example, if the temperature sensors become out of order and it is necessary to turn on the heating systems right now, but the server doesn't do it, you can send an **immediate command** and turn it on manually. In this case, it will be turned on untill you ask the server to get the rules back to work*.


It is possible to manage Hyrex AsQamm from three types of software:
- The PC client `AsQamm Dekstop`;
- The Android app `AsQamm Android`;
- Via an interactive screen (planned).

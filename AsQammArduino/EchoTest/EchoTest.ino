/*
 * Это скетч принимает строки вида
 * CMDn(arg1,arg2), где
 * CMDn — имя вызываемой команды,
 * arg1 и arg2 — необязательные аргументы.
 * 
 * Команда LEDo(mode) осуществляет управление
 * светодиодом на D13:
 *   param 'mode': int
 *     0 для выключения мигания, 1 для включения мигания
 */

#include <Firmata.h>

#include <jled.h>

auto led = JLed(13).Off().Forever();

void LEDo(unsigned int effect, unsigned int duration = 360) {
    //Команда LEDo(mode) осуществляет управление
    //светодиодом индикации на D13:
    //  param 'effect': int
    //    Выбор эффекта. Допустимы варианты:
    //    0 — отключить индикацию;
    //    1 — включить, эффект мигания;
    //    2 — включить, эффект "Дыхание";
    //    3 — включить, эффект "Свеча"
    //
    //  param 'duration': int = 360
    //    Длительность эффекта. Параметр
    //    игнорируется, если 'effect' = 0.

    if (effect == 0) led.Off().Forever();
    if (effect == 1) led.Blink(duration, duration).Forever();
    if (effect == 2) led.Breathe(duration).Forever();
    if (effect == 3) led.Candle().Forever();
}

unsigned long charIndex(const char * findIn, unsigned int symbol) {
    //Найти символ 'symbol' в массиве символов 'findIn'. В отличие от
    //strchr(), возвращает unsigned long

    char * pointer = strchr(findIn, symbol);
    if (pointer != NULL) return (pointer - findIn);
    if (pointer == NULL) return 0;
}

void stringCallback(char * received) {
    //Объявим необходимые переменные 
    char methodName[5];
    char argument1[5];
    char argument2[5];
    int commaLocation = 0;
    int lasti;

    //Количество читаемых символов в строке 'received' равно
    //индексу '\0' терминатора в этой строке
    byte nullTerminatorIndex = strlen(received);

    //Если строковая команда не соответствует синтаксису,
    //прервать работу функции и сообщить об ошибке
    if (!(received[4] == '(' && nullTerminatorIndex <= 15)) {
        Firmata.sendString("ERR;");
        return;
    }

    //Выделить имя вызываемого метода
    for (int i = 0; i < 4; i++) {
        methodName[i] = received[i];
    }
    methodName[4] = '\0';

    //Если есть аргументы:
    if (received[5] != ')') {
        //Проверим, есть ли запятая в команде
        if (charIndex(received, ',') != 0) commaLocation = charIndex(received, ',');

        //Если нет запятой, то записать аргумент
        //в argument1
        ;
        if (commaLocation == 0) {
            for (int i = 5; i < (nullTerminatorIndex - 1); i++) {
                argument1[(i - 5)] = received[i];
                lasti = (i - 5);
            }

            argument1[(lasti + 1)] = '\0';
            lasti = 0;
        }

        //Если запятая есть, то сначала записать
        //содержимое до запятой в argument1, а пос-
        //ле запятой — argument2
        if (commaLocation != 0) {
            //Запишем содержимое до запятой
            for (int i = 5; i < commaLocation; i++) {
                argument1[i - 5] = received[i];
                lasti = (i - 5);
            }

            argument1[(lasti + 1)] = '\0';
            lasti = 0;

            //Запишем содержимое после запятой
            for (int i = (commaLocation + 1); i < (nullTerminatorIndex - 1); i++) {
                argument2[(i - (commaLocation + 1))] = received[i];
                lasti = (i - (commaLocation + 1));
            }

            argument2[(lasti + 1)] = '\0';
            lasti = 0;
        }
    }

    if (strcmp(methodName, "LEDo") == 0) LEDo(atoi(argument1), atoi(argument2));
}

void sysexCallback(byte command, byte argc, byte * argv) {
    Firmata.sendSysex(command, argc, argv);
}

void setup() {
    Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);
    Firmata.attach(STRING_DATA, stringCallback);
    Firmata.attach(START_SYSEX, sysexCallback);
    Firmata.begin(57600);
}

void loop() {
    led.Update();

    while (Firmata.available()) {
        Firmata.processInput();
    }
}
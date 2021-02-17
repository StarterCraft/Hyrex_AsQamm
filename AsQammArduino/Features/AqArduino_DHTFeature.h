#pragma once
#include <Arduino.h>


void DHTt(const unsigned int pin, const unsigned int sensorType = 22) {
    //Команда опрашивает любой датчик
    //температуры вида DHT (DHT11, DHT22).
    //Отправляет обратно строку вида
    //"OK;{темпертура};{влажность}".
    //Используется код из https://clck.ru/TJyCA
    //
    //    param 'pin': int
    //        Пин, на котором расположен DHT.
    //
    //    param 'sensorType': int = 22
    //        Тип DHT. Допусимые значения: 11, 22

    static uint64_t prevMillis = 0;
    byte data[5];
    char catres[16], result[32];
    const unsigned int interval = 2000;
    int humidity, temperature;
    boolean returned;

    if (!(sensorType == 11 || sensorType == 22)) {
        Firmata.sendString("ERR;DHTt;SENS");
        return;
    }

    if (millis() - prevMillis > interval) {
        prevMillis += interval;

        //Допросим DHT
        byte duration = 0;
        byte j = 0;
        for (byte i = 0; i < 5; i++) {
            data[i] = 0;
        }
        pinMode(pin, OUTPUT);
        digitalWrite(pin, LOW);

        if (sensorType == 22) delay(1);                   //более 800mks нужно чтобы рабудить датчик DHT21-22
        if (sensorType == 11) delay(18);                  //для DHT11
        
        pinMode(pin, INPUT);                              //начинаем слушать датчик
        delayMicroseconds(50);
        for (byte i = 0; i < 41; i++) {                   //читаем 41 положительный импульс (первый неинформативный)
            duration = pulseIn(pin, HIGH, 200);
            if (!duration) break;
            if (i) {                                      //записываем сo 2 (i==1) импульса (1,?,?,...?)
                data[j / 8] <<= 1;                        //пишем в младший бит "0"
                if (duration > 50)
                    data[j / 8] |= 1;                     //пишем в младший бит "1"
                j++;
            }
        }

        uint8_t sum = data[0] + data[1] + data[2] + data[3];
        if (sum == data[4]) returned = true;
        else returned = false;

        //Пришёл ли ответ, или ошибка?
        if (returned) {
            humidity = (data[0] << 8) | data[1]; //считаем Н и Т первого датчика
            temperature = ((data[2] & 0x7F) << 8) | data[3];
            if (data[2] & 0x80)  temperature *= -1;

            //Отправляем результаты измерений
            strcpy(result, "OK;");
            strcat(result, itoa(temperature, catres, DEC));
            strncat(result, ";", 1);
            char catres[16];                              //Очищаем массив символов, переопределив его

            itoa(humidity, catres, DEC);
            strcat(result, itoa(humidity, catres, DEC));

            Firmata.sendString(result);
            return;
        } else {
            Firmata.sendString("ERR;DHTt;CSUM");
            return;
        }
    }
}

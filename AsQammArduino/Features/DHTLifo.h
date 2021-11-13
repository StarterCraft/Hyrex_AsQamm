#pragma once
#include <Arduino.h>


uint64_t readingTime;


void DHTt(const uint8_t pin) {
    if ((millis() - readingTime) > 2000) {
        unsigned char receivedDHTData[5];
        float temperature, humidity;

        #define DHT_PORT PORTD
        #define DHT_DDR DDRD
        #define DHT_PIN PIND
        #define DHT_BIT pin
        unint count = 32;
        unsigned char i, j;

        ReLoad: //метка для ошибок
        //=============MCU send START
        DHT_DDR |= (1 << DHT_BIT); //выход
        DHT_PORT &= ~(1 << DHT_BIT); //низкий уровень, подтягиваем линию, разбудим датчик
        delay(18); //18 мс по условиям документации.
        DHT_PORT |= (1 << DHT_BIT); //отпускаем линию
        DHT_DDR &= ~(1 << DHT_BIT); //пин как выход

        //============= инциализация DHT
        delayMicroseconds(50); //задержка по условию
        if (DHT_PIN & (1 << DHT_BIT)) { //датчик должен ответить 0
            if (count != 0) {
                goto ReLoad;
                count--;
            } else {
                Serial.println("ERR;DHTt;INIT");
                return;
            }
        }

        delayMicroseconds(80);
        if (!(DHT_PIN & (1 << DHT_BIT))) { //по истечению 80 мкс, датчик должен отпустить шину 
            if (count != 0) {
                goto ReLoad;
                count--;
            } else {
                Serial.println("ERR;DHTt;BHVR");
                return;
            }
        }

        //===============Приём 40 бит данных
        while (DHT_PIN & (1 << DHT_BIT)); //ждем пока на шине появится 1  
        for (j = 0; j < 5; j++) { //цикл для 0-4 байт
            receivedDHTData[j] = 0;
            for (i = 0; i < 8; i++) { //приём битов и укладка их в байты
                while (!(DHT_PIN & (1 << DHT_BIT))); //ждем когда датчик отпустит шину
                delayMicroseconds(30); //задержка высокого уровня при 0 30 мкс
                if (DHT_PIN & (1 << DHT_BIT)) //если по истечению времени сигнал на линии высокий, значит передается 1
                    receivedDHTData[j] |= 1 << (7 - i); //тогда i-й бит устанавливаем 1
                while (DHT_PIN & (1 << DHT_BIT)); //ждем окончание 1 
            }
        }

        if ((unsigned char)(receivedDHTData[0] + receivedDHTData[1] +
                receivedDHTData[2] + receivedDHTData[3]) != receivedDHTData[4]) { //checksum
            Serial.println("ERR;DHTt;CHSM");
            return;
        }

        // Температура есть 16-битное число со знаком
        // The temperature is a 16 bit signed integer, 10 times the actual value in degrees Celsius
        int16_t temperatureTimesTen = (int16_t)((receivedDHTData[2] << 8) | receivedDHTData[3]);
        temperature = (float)(temperatureTimesTen) * 0.1;
        if (receivedDHTData[2] & 0b10000000) temperature *= -1.0f; //если отрицательная температура
        //тупое решение проблемы
        if (temperature > 80) temperature = temperature - 3276.7f;

        humidity = (receivedDHTData[1] * 0.1) + (receivedDHTData[0] * 25.6); //нюанс расчета влажности для DHT22


        char result[64], catres[8];
        strcpy(result, "[0] ");
        itoa(receivedDHTData[0], catres, 2);
        strcat(result, catres);
        strcat(result, "; [1] ");
        itoa(receivedDHTData[1], catres, 2);
        strcat(result, catres);
        strcat(result, "; [2] ");
        itoa(receivedDHTData[2], catres, 2);
        strcat(result, catres);
        strcat(result, "; [3] ");
        itoa(receivedDHTData[3], catres, 2);
        strcat(result, catres);

        Serial.println(result);

        readingTime = millis();
        strcpy(result, "OK;DHTt;");

        dtostrf(temperature, 5, 1 catres);
        strcat(result, catres);
        strcat(result, ";");

        dtostrf(humidity, 5, 1, catres);
        strcat(result, catres);

        Serial.println(result);
        return;
    }
}
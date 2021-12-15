#pragma once
#define DHT22_MIN -40
#define DHT22_MAX 80
#include <Arduino.h>
#include <Firmata.h>


uint64_t readingTime;


void DHTt(const uint8_t pin) {
    if ((millis() - readingTime) > 2000) {
        unsigned char receivedDHTData[5];
        float temperature, humidity;

        #define DHT_PORT PORTD
        #define DHT_DDR DDRD
        #define DHT_PIN PIND
        #define DHT_BIT pin
        int count = 32;
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
                Firmata.sendString("ERR;DHTt;INIT");
                return;
            }
        }

        delayMicroseconds(80);
        if (!(DHT_PIN & (1 << DHT_BIT))) { //по истечению 80 мкс, датчик должен отпустить шину 
            if (count != 0) {
                goto ReLoad;
                count--;
            } else {
                Firmata.sendString("ERR;DHTt;BHVR");
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
            Firmata.sendString("ERR;DHTt;CHSM");
            return;
        }

        //Температура есть 16-битное число со знаком
        //The temperature is a 16 bit signed integer, 10 times the actual value in degrees Celsius
        temperature = ((receivedDHTData[2] & 0x7F) << 8 | receivedDHTData[3]) * 0.1;
        //if MSB = 1 we have negative temperature
        temperature = ((receivedDHTData[2] & 0x80) == 0 ? temperature : -temperature);

        //Если значение бессмысленно, попробуем другой метод извлечения
        if (temperature < DHT22_MIN || temperature > DHT22_MAX) {
            int32_t temp = ((receivedDHTData[2]) << 8 | receivedDHTData[3]);
            //if MSB = 1 we have negative temperature
            if (temp & 0x8000)
            {
                temp = temp | 0xFFFF0000; //sign-extend
                temperature = temp * 0.1f; //Convert to negative whole-degrees
            }
            else temperature = (float)temp / 10.0f;
        }

        humidity = (receivedDHTData[1] * 0.1) + (receivedDHTData[0] * 25.6); //нюанс расчета влажности для DHT22

        Serial.println(itoa(receivedDHTData[2]));
        Serial.println(itoa(receivedDHTData[3]));


        char result[32], catres[8];
        readingTime = millis();
        strcpy(result, "OK;DHTt;");

        dtostrf(temperature, 5, 2, catres);
        strcat(result, catres);
        strcat(result, ";");

        dtostrf(humidity, 5, 2, catres);
        strcat(result, catres);

        Firmata.sendString(result);
        return;
    }
}
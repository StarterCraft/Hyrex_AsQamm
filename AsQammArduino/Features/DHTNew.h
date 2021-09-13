#pragma once
#include <Arduino.h>
#include <Firmata.h>
#include <dhtnew.h>


uint64_t readingTime;


void DHTt(const uint8_t pin) {
    DHTNEW sensor(pin);
    char result[32], catres[8];
    boolean success = false;
    
    if ((millis() - readingTime) > 2000) {
        readingTime = millis();
        int chk = sensor.read();

        switch (chk) {
        case DHTLIB_OK:
            strcpy(result, "OK;DHTt;");
            success = true;
            break;
        case DHTLIB_ERROR_CHECKSUM:
            Firmata.sendString("ERR;DHTt;CHKS");
            break;
        case DHTLIB_ERROR_TIMEOUT_A:
            Firmata.sendString("ERR;DHTt;TIMA");
            break;
        case DHTLIB_ERROR_TIMEOUT_B:
            Firmata.sendString("ERR;DHTt;TIMB");
            break;
        case DHTLIB_ERROR_TIMEOUT_C:
            Firmata.sendString("ERR;DHTt;TIMC");
            break;
        case DHTLIB_ERROR_TIMEOUT_D:
            Firmata.sendString("ERR;DHTt;TIMD");
            break;
        case DHTLIB_ERROR_SENSOR_NOT_READY:
            Firmata.sendString("ERR;DHTt;SENR");
            break;
        case DHTLIB_ERROR_BIT_SHIFT:
            Firmata.sendString("ERR;DHTt;BITS");
            break;
        case DHTLIB_WAITING_FOR_READ:
            Firmata.sendString("ERR;DHTt;WAFR");
            break;
        default:
            strcpy(result, "ERR;DHTt;UNKN;");
            itoa(chk, catres, 10);
            strcat(result, catres);
            Firmata.sendString(result);
            break;
        }

        if (success) {
            readingTime = millis();
            dtostrf(sensor.getTemperature(), 5, 1, catres);
            strcat(result, catres);
            strcat(result, ";");

            dtostrf(sensor.getHumidity(), 5, 1, catres);
            strcat(result, catres);

            Firmata.sendString(result);
            return;

        } else {
            return; 
        }
    }
}
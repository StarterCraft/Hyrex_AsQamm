#pragma once
#include "Arduino.h"
#include <functional>
#include <map>

//Класс обработчика команд
class Processor {
    public:
        //Обработать входящую команду и понять, действительна ли она.
        //Если да, вызвать команду с аргументами 
        void processCommand(String received);

        //Привязать функцию, принимающую 1 аргумент типа long и возвращающую
        //long к ключевой строке из 4 символов. Допустимы символы A-Z и a-z.
        void attachIntCommand(String keystring, std::function<long(long)> function);

        //Привязать функцию, принимающую 1 аргумент типа long и возвращающую
        //double к ключевой строке из 4 символов. Допустимы символы A-Z и a-z.
        void attachDoubleCommend(String keystring, std::function<double(long)> function);

    private:
        //Словарь со всеми наименованиями команд, которые может выполнить
        //устройство. Заполняется методами attachIntCommand и attachDoubleCommand
        map <std::function, String> map;
};

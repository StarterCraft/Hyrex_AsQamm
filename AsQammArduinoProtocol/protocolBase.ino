String received[16];
bool receive = true;


void processCommand(String command) {
    if (!(command.length() >= 5 && command.length() <= 15 &&
        command[4] == '(' && (command [9] == ')' || command[14] == ')'))) {
        
        Serial.println("ERR;");
    }

    //Определять функции здесь
}


void setup()
{
    //Запускаем Serial
    Serial.begin(115200);
}


void loop() {
    //Если есть что принимать с Serial, 
    //и receive == истина, то записать
    //полученное в received и обработать
    //команду
    if (Serial.available() && receive) {
        received = (Serial.readString()).trim()       //.trim() убирает ненужные символы;
        receive = false;
    }
}

#include "AsQammProtocol.h"

void protocol::processCommand(String received){
	//Если строка действительна, продолжаем
	if ((received.length() >= 10) && (received.length() <= 15)) {

		//Эта функция обрабатывает строку,
		//полученную Serial, как команду.
		String expectedCommandPart;
		String expectedArgument;

		//Ñëàéñ ñòðîêè
		expectedCommandPart = String(
			received.charAt(0) +
			received.charAt(1) +
			received.charAt(2) +
			received.charAt(3));

		expectedArgument = String(
			received.charAt(5) +
			received.charAt(6) +
			received.charAt(7) +
			received.charAt(8));

		if (received.charAt(9) == ',' && received.length() > 10) {
			String expectedOptionalArgument;
			expectedOptionalArgument = String(
				received.charAt(10) +
				received.charAt(11) +
				received.charAt(12) +
				received.charAt(13));
		}
		
	}
}

#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 4, 1, 8, SW_UART_EVEN_PARITY);  //due_sw_uart *uart, int tx, int stopbits, int databits, int paritybit

}

void loop() {
 sw_uart_write_byte(&uart, 'z');  //CARCTERE A SER ENVIADO
 delay(10);
}

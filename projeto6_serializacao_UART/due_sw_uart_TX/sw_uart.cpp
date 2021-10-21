#include "sw_uart.h"
#pragma GCC optimize ("-O3")

void sw_uart_setup(due_sw_uart *uart, int tx, int stopbits, int databits, int paritybit) {
	
	uart->pin_tx     = tx;
	uart->stopbits   = stopbits;
	uart->paritybit  = paritybit;
  uart->databits   = databits;
  pinMode(tx, OUTPUT);
  digitalWrite(tx,HIGH);
}

int calc_even_parity(char data) {
  int ones = 0;

  for(int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }

  return ones % 2;
}


void sw_uart_write_byte(due_sw_uart *uart, char data){
  char letra = data;
  
  //start bit
  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);  

  //databits
  for(int i = 0; i < uart->databits; i++) {
    digitalWrite(uart->pin_tx, (letra >> i) & 0x01); //https://stackoverflow.com/questions/13823656/how-to-convert-char-to-an-array-of-bits-in-c/13823736
    _sw_uart_wait_T(uart);
  }

  

  //parity
  int parity = 0;
  if(uart->paritybit == SW_UART_EVEN_PARITY) {
     parity = calc_even_parity(letra);
  } else if(uart->paritybit == SW_UART_ODD_PARITY) {
     parity = !calc_even_parity(letra);
  }

  if(uart->paritybit != SW_UART_NO_PARITY) {
    digitalWrite(uart->pin_tx, parity);
    _sw_uart_wait_T(uart);
  }

  //stopbit
  for(int i = 0; i < uart->stopbits; i++) {
    digitalWrite(uart->pin_tx, HIGH); //estado padrão HIGH
    _sw_uart_wait_T(uart);
  }
}



// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart) {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart) {
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}

;*************************************************************************
; Title	:    I2C (Single) Master Implementation
; Author:    Peter Fleury <pfleury@gmx.ch>
;            based on Atmel Appl. Note AVR300
; File:      $Id: i2cmaster.S,v 1.14 2021/12/04 19:58:35 peter Exp $
; Software:  AVR-GCC 4.x
; Target:    any AVR device
;
; DESCRIPTION
; 	Basic routines for communicating with I2C slave devices. This
;	"single" master implementation is limited to one bus master on the
;	I2C bus. 
;  
;       Based on the Atmel Application Note AVR300, corrected and adapted 
;       to GNU assembler and AVR-GCC C call interface
;       Replaced the incorrect quarter period delays found in AVR300 with 
;       half period delays. 
;
; USAGE
;	These routines can be called from C, refere to file i2cmaster.h.
;       See example test_i2cmaster.c 
; 	Adapt the SCL and SDA port and pin definitions and eventually 
;	the delay routine to your target !
; 	Use 4.7k pull-up resistor on the SDA and SCL pin.
;
; NOTES
;	The I2C routines can be called either from non-interrupt or
;	interrupt routines, not both.
;
;*************************************************************************


#include <avr/io.h>

#undef SCL_PORT
#undef SCL_DDR


;******----- Adapt these SCA and SCL port and pin definition to your target !!
;
#define SDA             3           // SDA Port D, Pin 4   
#define SCL             4           // SCL Port D, Pin 5
#define SDA_PORT        PORTD       // SDA Port D
#define SCL_PORT        PORTD       // SCL Port D         

;******----------------------------------------------------------------------


;-- map the IO register back into the IO address space
#define SDA_DDR		(_SFR_IO_ADDR(SDA_PORT) - 1)
#define SCL_DDR		(_SFR_IO_ADDR(SCL_PORT) - 1)
#define SDA_OUT		_SFR_IO_ADDR(SDA_PORT)
#define SCL_OUT		_SFR_IO_ADDR(SCL_PORT)
#define SDA_IN		(_SFR_IO_ADDR(SDA_PORT) - 2)
#define SCL_IN		(_SFR_IO_ADDR(SCL_PORT) - 2)


#ifndef __tmp_reg__
#define __tmp_reg__ 0
#endif


	.section .text

;*************************************************************************
; delay half period
; For I2C in normal mode (100kHz), use T/2 > 5us
; For I2C in fast mode (400kHz),   use T/2 > 1.25us
;*************************************************************************
	.stabs	"",100,0,0,i2c_a_delay_T2
	.stabs	"i2cmaster.S",100,0,0,i2c_a_delay_T2
	.func i2c_a_delay_T2	; delay 5.0 microsec with 4 Mhz crystal	
i2c_a_delay_T2:        ; 3 cycles
#if F_CPU <= 4000000UL
	rjmp 1f      ; 2   "
1:	rjmp 2f      ; 2   "
2:	rjmp 3f      ; 2   "
3:	rjmp 4f      ; 2   "
4:	rjmp 5f      ; 2   "
5: 	rjmp 6f      ; 2   "
6:	nop          ; 1   "
	ret          ; 4   "  total 20 cyles = 5.0 microsec with 4 Mhz crystal 
#elif F_CPU <= 8000000UL
    push r24     ; 2 cycle
    ldi	 r24, 7  ; 1 cycle
	clr  r25     ; 1 cycle
1:	sbiw r24, 1  ; 2 cycle
	brne 1b      ; 2 or 1 cycle, 4 cycles per loop
	pop  r24     ; 2 ycle
	ret          ; 4 cycle = total 60 cycles = 5.0 microsec with 8 Mhz crystal
#elif F_CPU <= 12000000UL
    push r24     ; 2 cycle
    ldi	 r24, 12 ; 1 cycle
	clr  r25     ; 1 cycle
1:	sbiw r24, 1  ; 2 cycle
	brne 1b      ; 2 or 1 cycle, 4 cycles per loop
	pop  r24     ; 2 ycle
	ret          ; 4 cycle = total 60 cycles = 5.0 microsec with 12 Mhz crystal
#elif F_CPU <= 16000000UL
    push r24     ; 2 cycle
    ldi	 r24, 17 ; 1 cycle
	clr  r25     ; 1 cycle
1:	sbiw r24, 1  ; 2 cycle
	brne 1b      ; 2 or 1 cycle, 4 cycles per loop
	pop  r24     ; 2 ycle
	ret          ; 4 cycle = total 80 cycles = 5.0 microsec with 16 Mhz crystal
#else
    push r24     ; 2 cycle
    ldi	 r24, 22 ; 1 cycle
	clr  r25     ; 1 cycle
1:	sbiw r24, 1  ; 2 cycle
	brne 1b      ; 2 or 1 cycle, 4 cycles per loop
	pop  r24     ; 2 ycle
	ret          ; 4 cycle = total 100 cycles = 5.0 microsec with 20 Mhz crystal
#endif	
	.endfunc     ; 


;*************************************************************************
; Initialization of the I2C bus interface. Need to be called only once
; 
; extern void i2c_a_init(void)
;*************************************************************************
	.global i2c_a_init
	.func i2c_a_init
i2c_a_init:
	cbi SDA_DDR,SDA		;release SDA
	cbi SCL_DDR,SCL		;release SCL
	cbi SDA_OUT,SDA
	cbi SCL_OUT,SCL
	ret
	.endfunc


;*************************************************************************	
; Issues a start condition and sends address and transfer direction.
; return 0 = device accessible, 1= failed to access device
;
; extern unsigned char i2c_a_start(unsigned char addr);
;	addr = r24, return = r25(=0):r24
;*************************************************************************

	.global i2c_a_start
	.func   i2c_a_start
i2c_a_start:
	sbi 	SDA_DDR,SDA	;force SDA low
	rcall 	i2c_a_delay_T2	;delay T/2
	
	rcall 	i2c_a_write	;write address
	ret
	.endfunc		


;*************************************************************************
; Issues a repeated start condition and sends address and transfer direction.
; return 0 = device accessible, 1= failed to access device
;
; extern unsigned char i2c_a_rep_start(unsigned char addr);
;	addr = r24,  return = r25(=0):r24
;*************************************************************************

	.global i2c_a_rep_start
	.func	i2c_a_rep_start
i2c_a_rep_start:
	sbi	SCL_DDR,SCL	;force SCL low
	rcall 	i2c_a_delay_T2	;delay  T/2
	cbi	SDA_DDR,SDA	;release SDA
	rcall	i2c_a_delay_T2	;delay T/2
	cbi	SCL_DDR,SCL	;release SCL
	rcall 	i2c_a_delay_T2	;delay  T/2
	sbi 	SDA_DDR,SDA	;force SDA low
	rcall 	i2c_a_delay_T2	;delay	T/2
	
	rcall	i2c_a_write	;write address
	ret
	.endfunc


;*************************************************************************	
; Issues a start condition and sends address and transfer direction.
; If device is busy, use ack polling to wait until device is ready
;
; extern void i2c_a_start_wait(unsigned char addr);
;	addr = r24
;*************************************************************************

	.global i2c_a_start_wait
	.func   i2c_a_start_wait
i2c_a_start_wait:
	mov	__tmp_reg__,r24
i2c_a_start_wait1:
	sbi 	SDA_DDR,SDA	;force SDA low
	rcall 	i2c_a_delay_T2	;delay T/2
	mov	r24,__tmp_reg__
	rcall 	i2c_a_write	;write address
	tst	r24		;if device not busy -> done
	breq	i2c_a_start_wait_done
	rcall	i2c_a_stop	;terminate write operation
	rjmp	i2c_a_start_wait1	;device busy, poll ack again
i2c_a_start_wait_done:
	ret
	.endfunc	


;*************************************************************************
; Terminates the data transfer and releases the I2C bus
;
; extern void i2c_a_stop(void)
;*************************************************************************

	.global	i2c_a_stop
	.func	i2c_a_stop
i2c_a_stop:
	sbi	SCL_DDR,SCL	;force SCL low
	sbi	SDA_DDR,SDA	;force SDA low
	rcall	i2c_a_delay_T2	;delay T/2
	cbi	SCL_DDR,SCL	;release SCL
	rcall	i2c_a_delay_T2	;delay T/2
	cbi	SDA_DDR,SDA	;release SDA
	rcall	i2c_a_delay_T2	;delay T/2
	ret
	.endfunc


;*************************************************************************
; Send one byte to I2C device
; return 0 = write successful, 1 = write failed
;
; extern unsigned char i2c_a_write( unsigned char data );
;	data = r24,  return = r25(=0):r24
;*************************************************************************
	.global i2c_a_write
	.func	i2c_a_write
i2c_a_write:
	sec			;set carry flag
	rol 	r24		;shift in carry and out bit one
	rjmp	i2c_a_write_first
i2c_a_write_bit:
	lsl	r24		;if transmit register empty
i2c_a_write_first:
	breq	i2c_a_get_ack
	sbi	SCL_DDR,SCL	;force SCL low
	brcc	i2c_a_write_low
	nop
	cbi	SDA_DDR,SDA	;release SDA
	rjmp	i2c_a_write_high
i2c_a_write_low:
	sbi	SDA_DDR,SDA	;force SDA low
	rjmp	i2c_a_write_high
i2c_a_write_high:
	rcall 	i2c_a_delay_T2	;delay T/2
	cbi	SCL_DDR,SCL	;release SCL
	rcall	i2c_a_delay_T2	;delay T/2
	rjmp	i2c_a_write_bit
	
i2c_a_get_ack:
	sbi	SCL_DDR,SCL	;force SCL low
	cbi	SDA_DDR,SDA	;release SDA
	rcall	i2c_a_delay_T2	;delay T/2
	cbi	SCL_DDR,SCL	;release SCL
i2c_a_ack_wait:
	sbis	SCL_IN,SCL	;wait SCL high (in case wait states are inserted)
	rjmp	i2c_a_ack_wait
	
	clr	r24		;return 0
	sbic	SDA_IN,SDA	;if SDA high -> return 1
	ldi	r24,1
	rcall	i2c_a_delay_T2	;delay T/2
	clr	r25
	ret
	.endfunc



;*************************************************************************
; read one byte from the I2C device, send ack or nak to device
; (ack=1, send ack, request more data from device 
;  ack=0, send nak, read is followed by a stop condition)
;
; extern unsigned char i2c_a_read(unsigned char ack);
;	ack = r24, return = r25(=0):r24
; extern unsigned char i2c_a_readAck(void);
; extern unsigned char i2c_a_readNak(void);
; 	return = r25(=0):r24
;*************************************************************************
	.global i2c_a_readAck
	.global i2c_a_readNak
	.global i2c_a_read		
	.func	i2c_a_read
i2c_a_readNak:
	clr	r24
	rjmp	i2c_a_read
i2c_a_readAck:
	ldi	r24,0x01
i2c_a_read:
	ldi	r23,0x01	;data = 0x01
i2c_a_read_bit:
	sbi	SCL_DDR,SCL	;force SCL low
	cbi	SDA_DDR,SDA	;release SDA (from previous ACK)
	rcall	i2c_a_delay_T2	;delay T/2
	
	cbi	SCL_DDR,SCL	;release SCL
	rcall	i2c_a_delay_T2	;delay T/2
	
i2c_a_read_stretch:
    sbis SCL_IN, SCL        ;loop until SCL is high (allow slave to stretch SCL)
    rjmp	i2c_a_read_stretch
    	
	clc			;clear carry flag
	sbic	SDA_IN,SDA	;if SDA is high
	sec			;  set carry flag
	
	rol	r23		;store bit
	brcc	i2c_a_read_bit	;while receive register not full
	
i2c_a_put_ack:
	sbi	SCL_DDR,SCL	;force SCL low	
	cpi	r24,1
	breq	i2c_a_put_ack_low	;if (ack=0)
	cbi	SDA_DDR,SDA	;      release SDA
	rjmp	i2c_a_put_ack_high
i2c_a_put_ack_low:                ;else
	sbi	SDA_DDR,SDA	;      force SDA low
i2c_a_put_ack_high:
	rcall	i2c_a_delay_T2	;delay T/2
	cbi	SCL_DDR,SCL	;release SCL
i2c_a_put_ack_wait:
	sbis	SCL_IN,SCL	;wait SCL high
	rjmp	i2c_a_put_ack_wait
	rcall	i2c_a_delay_T2	;delay T/2
	mov	r24,r23
	clr	r25
	ret
	.endfunc


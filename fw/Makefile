MCU=atmega1284p
DEFINES=-DF_CPU=20000000UL
PROGRAMMER_MCU=m1284p
PROJECTNAME=ictester
PRJSRC=ictester.c serial.c zif.c led.c protocol.c logic.c mem.c univib.c \
       external/pololu-led-strip-avr/led_strip.c \
       external/fleury-i2cmaster/i2cmaster_a.S external/fleury-i2cmaster/i2cmaster_b.S
INC=
LIBS=
OPTLEVEL=3
HEXFORMAT=ihex

# compiler
CFLAGS=-I. $(INC) -g -mmcu=$(MCU) -O$(OPTLEVEL) \
        -std=gnu99 $(DEFINES) -flto             \
	--param=min-pagesize=0                  \
	-fpack-struct -fshort-enums             \
	-funsigned-bitfields -funsigned-char    \
	-Wall -Wstrict-prototypes

# c++ specific flags
CPPFLAGS=-fno-exceptions

# assembler
ASMFLAGS =-I. $(INC) -mmcu=$(MCU)        \
	-x assembler-with-cpp -flto      \
	-Wa,-gstabs,-ahlms=$(firstword   \
	$(<:.S=.lst) $(<.s=.lst))

# linker
LDFLAGS=-Wl,-Map,$(TRG).map -mmcu=$(MCU) \
	-flto -lm $(LIBS)

##### executables ####
CC=avr-gcc
OBJCOPY=avr-objcopy
OBJDUMP=avr-objdump
SIZE=avr-size
AVRDUDE=avrdude
REMOVE=rm -f

##### automatic target names ####
TRG=$(PROJECTNAME).out
DUMPTRG=$(PROJECTNAME).s

HEXROMTRG=$(PROJECTNAME).hex 
HEXTRG=$(HEXROMTRG) $(PROJECTNAME).ee.hex
GDBINITFILE=gdbinit-$(PROJECTNAME)

# Define all object files.

CPPFILES=$(filter %.cpp, $(PRJSRC))
CCFILES=$(filter %.cc, $(PRJSRC))
BIGCFILES=$(filter %.C, $(PRJSRC))
CFILES=$(filter %.c, $(PRJSRC))
ASMFILES=$(filter %.S, $(PRJSRC))


# List all object files we need to create
OBJDEPS=$(CFILES:.c=.o)    \
	$(CPPFILES:.cpp=.o)\
	$(BIGCFILES:.C=.o) \
	$(CCFILES:.cc=.o)  \
	$(ASMFILES:.S=.o)

# Define all lst files.
LST=$(filter %.lst, $(OBJDEPS:.o=.lst))

# All the possible generated assembly 
# files (.s files)
GENASMFILES=$(filter %.s, $(OBJDEPS:.o=.s)) 


.SUFFIXES : .c .cc .cpp .C .o .out .s .S \
	.hex .ee.hex .h .hh .hpp


.PHONY: writeflash clean stats gdbinit stats

# Make targets:
# all, disasm, stats, hex, writeflash/install, clean
all: $(TRG)

disasm: $(DUMPTRG) stats

stats: $(TRG)
	$(SIZE) $(TRG) 

hex: $(HEXTRG)

.check-programmer-var:
	@test -n "$${AVRDUDE_PROGRAMMER}" || (echo Please set environment variable AVRDUDE_PROGRAMMER to define options for your programmer \(eg. \"-c stk500v2 -P avrdoper\"\) && exit 1)

writeflash: hex .check-programmer-var
	$(AVRDUDE) $(AVRDUDE_PROGRAMMER) -p $(PROGRAMMER_MCU) -e -U flash:w:$(HEXROMTRG)

fuses: .check-programmer-var
	$(AVRDUDE) $(AVRDUDE_PROGRAMMER) -p $(PROGRAMMER_MCU) -U lfuse:w:0xff:m -U hfuse:w:0xd9:m -U efuse:w:0xff:m

reset: .check-programmer-var
	$(AVRDUDE) $(AVRDUDE_PROGRAMMER) -p $(PROGRAMMER_MCU)

install: writeflash

$(DUMPTRG): $(TRG) 
	$(OBJDUMP) -S  $< > $@


$(TRG): $(OBJDEPS) 
	$(CC) $(LDFLAGS) -o $(TRG) $(OBJDEPS)


#### Generating assembly ####
# asm from C
%.s: %.c
	$(CC) -S $(CFLAGS) $< -o $@

# asm from (hand coded) asm
%.s: %.S
	$(CC) -S $(ASMFLAGS) $< > $@


# asm from C++
.cpp.s .cc.s .C.s :
	$(CC) -S $(CFLAGS) $(CPPFLAGS) $< -o $@



#### Generating object files ####
# object from C
.c.o: 
	$(CC) $(CFLAGS) -c $< -o $@


# object from C++ (.cc, .cpp, .C files)
.cc.o .cpp.o .C.o :
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

# object from asm
.S.o :
	$(CC) $(ASMFLAGS) -c $< -o $@


#### Generating hex files ####
# hex files from elf
#####  Generating a gdb initialisation file    #####
.out.hex:
	$(OBJCOPY) -j .text -j .data -O $(HEXFORMAT) $< $@

.out.ee.hex:
	$(OBJCOPY) -j .eeprom --change-section-lma .eeprom=0 -O $(HEXFORMAT) $< $@


#####  Generating a gdb initialisation file    #####
##### Use by launching simulavr and avr-gdb:   #####
#####   avr-gdb -x gdbinit-myproject           #####
gdbinit: $(GDBINITFILE)

$(GDBINITFILE): $(TRG)
	@echo "file $(TRG)" > $(GDBINITFILE)
	
	@echo "target remote localhost:1212" >> $(GDBINITFILE)
	
	@echo "load"        >> $(GDBINITFILE) 
	@echo "break main"  >> $(GDBINITFILE)
	@echo "continue"    >> $(GDBINITFILE)
	@echo
	@echo "Use 'avr-gdb -x $(GDBINITFILE)'"


#### Cleanup ####
clean:
	$(REMOVE) $(TRG) $(TRG).map $(DUMPTRG)
	$(REMOVE) $(OBJDEPS)
	$(REMOVE) $(LST) $(GDBINITFILE)
	$(REMOVE) $(GENASMFILES)
	$(REMOVE) $(HEXTRG)


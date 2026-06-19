CC ?= gcc
CFLAGS ?= -fPIC -Wall -O2

.PHONY: all clean

all: libadd.so

libadd.so: add.c
	$(CC) $(CFLAGS) -shared -o libadd.so add.c

clean:
	rm -f libadd.so

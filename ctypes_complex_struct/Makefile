CC = gcc
CFLAGS = -Wall -Wextra -fPIC -O2
TARGET = libstruct_demo.so
SOURCES = struct_demo.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SOURCES) struct_demo.h
	$(CC) $(CFLAGS) -shared -o $(TARGET) $(SOURCES)

clean:
	rm -f $(TARGET)

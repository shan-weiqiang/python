CXX = g++
CXXFLAGS = -std=c++17 -fPIC -Wall -Wextra -Icpp
LDFLAGS = -shared

TARGET = libhandle_bridge.so
SOURCES = cpp/handle_pool.cpp cpp/config.cpp cpp/counter.cpp \
          cpp/config_snapshot_resource.cpp cpp/process_summary_resource.cpp \
          cpp/counter_stats_resource.cpp cpp/bridge.cpp

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $(TARGET) $(SOURCES)

clean:
	rm -f $(TARGET)

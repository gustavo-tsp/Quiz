CC      = gcc
CFLAGS  = -Wall -Wextra -O2
BUILD   = build

UNAME := $(shell uname -s)
ifeq ($(UNAME),Darwin)
    LIBEXT = dylib
else
    LIBEXT = so
endif

all: $(BUILD)/libmathlib.$(LIBEXT) $(BUILD)/main_c

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/libmathlib.$(LIBEXT): c/mathlib.c c/mathlib.h | $(BUILD)
	$(CC) $(CFLAGS) -shared -fPIC -o $@ c/mathlib.c

$(BUILD)/main_c: c/main.c c/mathlib.c c/mathlib.h | $(BUILD)
	$(CC) $(CFLAGS) -o $@ c/main.c c/mathlib.c

run-c: all
	./$(BUILD)/main_c

run-py: all
	python3 python/main.py

test: all
	python3 -m unittest discover -s tests -v

clean:
	rm -rf $(BUILD)

.PHONY: all run-c run-py test clean

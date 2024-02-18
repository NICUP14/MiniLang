# Project structure
RECIPE ?=
BUILD_DIR ?= bin
SOURCE_DIR ?= src

# Project parameters
PROJECT = main
SOURCES = $(wildcard $(SOURCE_DIR)/*.ml)
OBJECTS = $(patsubst $(SOURCE_DIR)/%.ml, $(BUILD_DIR)/%.o, $(SOURCES))
ASM_OBJECTS = $(patsubst $(SOURCE_DIR)/%.ml, $(BUILD_DIR)/%.S, $(SOURCES))

# C compiler parameters
CC = gcc
CFLAGS ?=
CLAGS += -g

# Compiler parameters
ML = python ../../src/Main.py
MLLIB ?= "../../include"
MLFLAGS ?=
MLFLAGS += -C

# Recipes
default: clean assemble
debug: clean _debug
assemble: $(ASM_OBJECTS)
compile: $(PROJECT)

# Shortcuts
def: default
dbg: debug
asm: assemble

_debug:
	$(ML) $(MLFLAGS) -d -I $(MLLIB) -I src $(SOURCES)

$(PROJECT) : $(OBJECTS)
	$(CC) $(CFLAGS) $(CXX) $^ -o $(BUILD_DIR)/$@

$(BUILD_DIR)/%.o: $(BUILD_DIR)/%.S
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $^ -o $@

$(BUILD_DIR)/%.S: $(SOURCE_DIR)/%.ml
	@mkdir -p $(BUILD_DIR)
	$(ML) $(MLFLAGS) -I $(MLLIB) -I src $< -o $@

clean:
	@rm -vrf $(BUILD_DIR)
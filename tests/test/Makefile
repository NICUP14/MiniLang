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
default: clean def
debug: clean _debug
assemble: $(ASM_OBJECTS)
compile: $(PROJECT)

# Shortcuts
def: _c
dbg: debug
cdbg: _cdebug
c: _c
asm: assemble


_c:
	@mkdir -p $(BUILD_DIR)
	$(ML) $(MLFLAGS) -I $(MLLIB) -I src src/main.ml -o $(BUILD_DIR)/$(PROJECT).c
	# $(ML) $(MLFLAGS) -I $(MLLIB) -I src src/main.ml > $(BUILD_DIR)/$(PROJECT).c
	$(CC) $(BUILD_DIR)/$(PROJECT).c -o $(BUILD_DIR)/$(PROJECT)

_cdebug:
	$(ML) $(MLFLAGS) -I $(MLLIB) -I src $(SOURCES)

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
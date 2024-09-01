# Project structure
RECIPE ?=
BUILD_DIR ?= bin
SOURCE_DIR ?= src

# Project parameters
PROJECT = main
SOURCES = $(wildcard $(SOURCE_DIR)/main.ml)
OBJECTS = $(patsubst $(SOURCE_DIR)/%.ml, $(BUILD_DIR)/%.c, $(SOURCES))
ASM_OBJECTS = $(patsubst $(SOURCE_DIR)/%.ml, $(BUILD_DIR)/%.S, $(SOURCES))

# C compiler parameters
CC = gcc
CFLAGS ?=
CFLAGS += -g

# Compiler parameters
ML = python ../../src/Main.py
MLLIB ?= "../../include"
MLFLAGS ?=
MLFLAGS += -C -c

# Recipes
default: clean def
c: clean _c
ml: clean _ml
debug: clean _mldebug
cdebug: clean _cdebug
assemble: $(ASM_OBJECTS)
compile: $(PROJECT)

# Shortcuts
def: c
dbg: debug
cdbg: cdebug
asm: assemble

_c: $(SOURCES)
	@mkdir -p $(BUILD_DIR)
	$(ML) $(MLFLAGS) -I $(MLLIB) -I src $(SOURCES) > $(BUILD_DIR)/$(PROJECT).c
	$(CC) $(CFLAGS) -I include include/*.c $(BUILD_DIR)/$(PROJECT).c -o $(BUILD_DIR)/$(PROJECT)

_cdebug: $(SOURCES)
	$(ML) $(MLFLAGS) -I $(MLLIB) -I src $(SOURCES)

_ml:
	@mkdir -p $(BUILD_DIR)
	$(ML) $(MLFLAGS) -d -I $(MLLIB) -I src $(SOURCES) -o $(BUILD_DIR)/$(PROJECT).ml

_mldebug: $(SOURCES)
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
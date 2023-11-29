#!/bin/bash

export MINT_BOX_LOC="$HOME/Documents/Mint\ Box/ML"

alias pm="python Main.py -o main.S"
# shellcheck disable=SC2139
alias cpm="[ ! -d $MINT_BOX_LOC ] && mkdir $MINT_BOX_LOC; cp main.S $MINT_BOX_LOC"

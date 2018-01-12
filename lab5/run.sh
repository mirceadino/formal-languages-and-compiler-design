#!/bin/bash

if [ $# -lt 1 ]; then
  python3 -B main.py
  exit 1
fi

flex lexer.lx
gcc -ll lex.yy.c
./a.out < $1 > pif
rm a.out
rm lex.yy.c

python3 -B main.py pif

rm pif

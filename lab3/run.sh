#!/bin/bash

flex lexer.lx
gcc -ll lex.yy.c
./a.out < $1
rm a.out

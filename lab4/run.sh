#!/bin/bash

flex lexer.lx
yacc -d parser.y
gcc -ll lex.yy.c y.tab.c
./a.out < $1
rm a.out
rm lex.yy.c y.tab.h y.tab.c

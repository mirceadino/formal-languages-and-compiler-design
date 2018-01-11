%{

#include <stdio.h>

int yyerror(const char* s);
extern int yylex(void);
extern void show();

%}

%start program

%token <val> IDENTIFIER
%token <val> CONSTANT
%token TYPE
%token IF
%token ELSE
%token WHILE
%token CIN
%token CIN_OP
%token COUT
%token COUT_OP 

%left ADD SUBSTRACT
%left MULTIPLY DIVIDE MODULO
%left BOOL

%%

program: declaration_list statement_list;
declaration_list: 
                | variable_declaration declaration_list;
variable_declaration: TYPE IDENTIFIER ';'
                    | TYPE IDENTIFIER '=' expression ';';
statement_list: 
              | statement statement_list;
statement: assignment_statement ';'
         | io_statement ';'
         | if_statement ';'
         | while_statement;
assignment_statement: IDENTIFIER '=' expression;
expression: term 
          | term add_sub_operator expression;
add_sub_operator: ADD | SUBSTRACT;
term: factor 
    | factor mul_div_mod_operator term;
mul_div_mod_operator: MULTIPLY | DIVIDE | MODULO;
factor: numeral 
      | '(' expression ')';
numeral: CONSTANT 
       | IDENTIFIER;
io_statement: read_statement 
            | write_statement;
read_statement: CIN CIN_OP IDENTIFIER;
write_statement: COUT COUT_OP numeral;
if_statement: IF '(' condition ')' '{' statement_list '}' 
            | IF '(' condition ')' '{' statement_list '}' ELSE '{' statement_list '}'
condition: expression BOOL expression
while_statement: WHILE '(' condition ')' '{' statement_list '}'

%%

int main(int argc, char** argv) {
  yyparse();
  show();
}

int yyerror(const char* s) {
  fprintf(stderr, "Error: %s\n", s);
  return -1;
}

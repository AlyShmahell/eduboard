%{
#include <stdio.h>
#include <stdlib.h>
#include "switch.lexer.c"
int errors = 0;
%}
%union
{
  int ival;
  char cval[10];
  float fval;
}
%token DEC_INT DEC_CHAR DEC_REAL DEC_CHAIN EQ SEMI
%token ID
%token <ival> NUM
%token <fval> REAL
%token <cval> CHAR
%token <cval> CHAIN
%right EQ
%start st
%%
st:declaration expression;
declaration:
|decl_type ident expression;
decl_type:DEC_INT
|DEC_REAL
|DEC_CHAR
|DEC_CHAIN;
ident:ID| ID ident;
expression: 
|SEMI expression
|ID EQ ID SEMI expression
|ID EQ CHAIN SEMI expression
|ID EQ CHAR SEMI expression
|ID EQ NUM SEMI expression
|ID EQ REAL SEMI expression
|EQ ID SEMI expression
|EQ CHAIN SEMI expression
|EQ CHAR SEMI expression
|EQ NUM SEMI expression
|EQ REAL SEMI expression;
%%
int yyerror (char *s)
{
  errors++;
  printf("Error:: %d %s at line:: %d in statement:: %s\n",errors,s,line,yytext);}
int yywrap(){return 1;}
int main()
{
  if((yyin=fopen("input.txt","r"))==NULL)
    {
      printf("input.txt not found !\n");
      return 0;
    }
  yyparse();
  if(!errors) printf("Ok\n");
  return 0;
}

%{
#include <stdio.h>
#include <stdlib.h>
#include "Typedef.lexer.c"
#include "Symb.h"
int errors = 0;
int curr_type;

void setup_symb(char* s, int type)
{ 
  if(put_symb(s,type)==0)
    yyerror(" Identifier is defined previously: ");
  return;
}

void check_symb(char* s)
{
  if(get_symb(s)==0)
    yyerror(" Identifier is unknown: ");
  return;
}
%}
%union
{
  int ival;
  char cval[10];
  float fval;
  char id[90];
}
%token DEC_INT DEC_CHAR DEC_REAL DEC_CHAIN EQ SEMI
%token <id> ID
%token <ival> NUM
%token <fval> REAL
%token <cval> CHAR
%token <cval> CHAIN
%right EQ
%start st
%%
st: 
|declaration expression
;
declaration: 
|decl_type ident SEMI declaration
|decl_type ident SEMI expression
;
decl_type:DEC_INT	{curr_type=_int;}
|DEC_REAL		{curr_type=_real;}
|DEC_CHAR		{curr_type=_char;}
|DEC_CHAIN		{curr_type=_chain;}
;
ident:ID	{setup_symb($1,curr_type);}
|ID ident	{setup_symb($1,curr_type);}
;
expression: 
|exp
|exp expression
|exp declaration
;
exp: 
|ID EQ ID SEMI		{check_symb($1); check_symb($3);if(get_type($1)!=get_type($3)) yyerror(" Incompatible EQ ");}
|ID EQ CHAIN SEMI	{check_symb($1);if(get_type($1)!=4) yyerror(" Incompatible Type Chain ");}
|ID EQ CHAR SEMI	{check_symb($1);if(get_type($1)!=3) yyerror(" Incompatible Type Char ");}
|ID EQ NUM SEMI		{check_symb($1);if(get_type($1)!=1) yyerror(" Incompatible Type Int ");}
|ID EQ REAL SEMI	{check_symb($1);if(get_type($1)!=2) yyerror(" Incompatible Type Float ");}
;
%%

int yyerror (char *s)
{
  errors++;
  printf("Error:: %d %s at line:: %d in statement:: %s\n",errors,s,line,yytext);
}

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

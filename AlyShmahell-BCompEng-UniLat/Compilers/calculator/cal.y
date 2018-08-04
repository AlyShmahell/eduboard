%{
#include <stdio.h>
#include <stdlib.h>
#include "cal.lexer.c"
    extern FILE* yyin;
%}

%token NUMBER PLUS MINUS MULT DIV POWER PARL PARR EQUAL
%left PLUS MINUS
%left MULT DIV
%left NEG
%right POWER
%start Input

%%
Input: 
| Input Line
;
Line: EQUAL
| EXP EQUAL	{printf("%d\n",$1);}
;
EXP: NUMBER	{ $$ = $1; }
| EXP PLUS EXP	{ $$ = $1 + $3; }
| EXP MINUS EXP	{ $$ = $1 - $3; }
| EXP MULT EXP	{ $$ = $1 * $3; }
| EXP DIV EXP	{ $$ = $1 / $3; }
| MINUS EXP %prec NEG	{ $$ = - $2; }
| EXP POWER EXP	{ $$ = poww($1,$3); }
| PARL EXP PARR	{ $$ = $2; }
;
%%

int poww(int base, int power)
{
    int temp=1;
    while(power--)
        temp*=base;
    return temp;
}

void yyerror(const char* s)
{
    fprintf(stderr, "Parse error: %s\n", s);
    exit(1);
}

int yywrap()
{
    return 1;
}

int main()
{
    yyin = stdin;

    do
    {
        yyparse();
    }
    while(!feof(yyin));

    return 0;
}

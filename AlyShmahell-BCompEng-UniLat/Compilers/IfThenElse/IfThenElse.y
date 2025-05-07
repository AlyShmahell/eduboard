%{
#include <stdio.h>
#include <stdlib.h>
#include "IfThenElse.lexer.c"
int errors = 0;
int sem_error=0;
    extern FILE* yyin;
%}

%token NUMBER PLUS MINUS MULT DIV POWER PARL PARR EQUAL ID IF THEN ELSE ASSIGN LT GT LE GE AND OR NE SEMI
%right EQUAL
%left AND OR
%left LE GE LT GT EQ NE
%left PLUS MINUS
%left MULT DIV
%left NEG
%right POWER
%start Start

%%
Start: Stmnt	{printf("input accepted\n");exit(0);}
;
Stmnt: IF PARL Con PARR THEN St1 SEMI ELSE St1 SEMI
| IF PARL Con PARR THEN St1 SEMI
;
St1: Stmnt
| EXP	{printf("result is : %d\n",$1);}
;
EXP: NUMBER	{ $$ = $1; }
| ID { $$ = $1; }
| EXP PLUS EXP	{ $$ = $1 + $3; }
| EXP MINUS EXP	{ $$ = $1 - $3; }
| EXP MULT EXP	{ $$ = $1 * $3; }
| EXP DIV EXP	{ $$ = $1 / $3; }
| MINUS EXP %prec NEG	{ $$ = - $2; }
| EXP POWER EXP	{ $$ = poww($1,$3); }
| PARL EXP PARR	{ $$ = $2; }
| EXP LT EXP	{if($1<$3) $$ = 1; else $$ = 0;}
| EXP GT EXP	{if($1>$3) $$ = 1; else $$ = 0;}
| EXP LE EXP	{if($1<=$3) $$ = 1; else $$ = 0;}
| EXP GE EXP	{if($1>=$3) $$ = 1; else $$ = 0;}
| EXP EQ EXP	{if($1==$3) $$ = 1; else $$ = 0;}
| EXP NE EXP	{if($1!=$3) $$ = 1; else $$ = 0;}
| EXP OR EXP	{if($1||$3) $$ = 1; else $$ = 0;}
| EXP AND EXP	{if($1&&$3) $$ = 1; else $$ = 0;}
;
Con: EXP LT EXP
| EXP GT EXP	{if($1>$3) return 1; else {sem_error=1155;return 0;}}
| EXP LT EXP	{if($1<$3) return 1; else {sem_error=1155;return 0;}}
| EXP GE EXP	{if($1>=$3) return 1; else {sem_error=1155;return 0;}}
| EXP EQ EXP	{if($1==$3) return 1; else {sem_error=1155;return 0;}}
| EXP NE EXP	{if($1!=$3) return 1; else {sem_error=1155;return 0;}}
| EXP OR EXP	{if($1||$3) return 1; else {sem_error=1155;return 0;}}
| EXP AND EXP	{if($1&&$3) return 1; else {sem_error=1155;return 0;}}
| ID		{if($1>0) return 1; else {sem_error=1155;return 0;}}
| NUMBER	{if($1>0) return 1; else {sem_error=1155;return 0;}}
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
    if(sem_error==1155)
      {
       fprintf(stderr, "wrong if statement\n");
       exit(1);
      }
    else
      {
       errors++;
       fprintf(stderr, "Parse error %d: %s at line %d, in statement: %s \n",errors,s,line,yytext);
       exit(1);
      }
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

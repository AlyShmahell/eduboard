%{
#include <stdio.h>
#include "IfThenElse.tokens.h"
int line = 1;
%}

%%
"if"		return IF;
"else"		return ELSE;
"then"		return THEN;
[ \t]+		;
[0-9]+		{yylval= atoi(yytext); return NUMBER;};
[a-zA-Z]	{return ID;}
"+"		{return PLUS;}
"-"		{return MINUS;}
"*"		{return MULT;}
"/"		{return DIV;}
"=="		{return EQ;}
"^"		{return POWER;}
"("		{return PARL;}
")"		{return PARR;}
"\n"		{line++;}
";"		return SEMI;
"<"		return LT;
">"		return GT;
"<="		return LE;
">="		return GE;
"!="		return NE;
"||"		return OR;
"&&"		return AND;
%%

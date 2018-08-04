%{
#include <stdio.h>
#include "cal.tokens.h"
%}

%%
[ \t]		;
[0-9]+		{yylval= atoi(yytext); return NUMBER;};
"+"		{return PLUS;}
"-"		{return MINUS;}
"*"		{return MULT;}
"/"		{return DIV;}
"="		{return EQUAL;}
"^"		{return POWER;}
"("		{return PARL;}
")"		{return PARR;}
%%

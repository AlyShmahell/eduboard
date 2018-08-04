%{
#include <stdio.h>
#include <string.h>
#include "switch.tokens.h"
int line = 1;
%}

alpha [a-zA-Z]
digit [0-9]+
blanc [ \t]+
rdigit {digit}\.{digit}
ident {alpha}({alpha}|{digit})*
a [aA]
b [bB]
c [cC]
d [dD]
e [eE]
f [fF]
g [gG]
h [hH]
i [iI]
j [jJ]
k [kK]
l [lL]
m [mM]
n [nN]
o [oO]
p [pP]
q [qQ]
r [rR]
s [sS]
t [tT]
u [uU]
v [vV]
w [wW]
x [xX]
y [yY]
z [zZ]

%%

{blanc}
\n	{ line++; };
"int"	return(DEC_INT);
real	return(DEC_REAL);
char	return(DEC_CHAR);
chain	return(DEC_CHAIN);
"="	return EQ;
"\""."\""	return(CHAR);
"\""(.)+"\""	return(CHAIN);
";"	return(SEMI);
{digit}+	{yylval.ival=atoi(yytext); return(NUM);};
{rdigit}	{yylval.fval=atof(yytext); return(REAL);};
{ident}		{strcpy(yylval.cval,yytext); return(ID);};


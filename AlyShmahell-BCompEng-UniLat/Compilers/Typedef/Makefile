compile: Typedef.l Typedef.y
	# calling flex
	flex Typedef.l
	# copying lex.yy.c to Typedef.lexer.c
	cp lex.yy.c Typedef.lexer.c
	# removing lex.yy.c
	rm lex.yy.c
	# calling bison
	bison -d Typedef.y
	# copying Typedef.tab.h to Typedef.tokens.h
	cp Typedef.tab.h Typedef.tokens.h
	# removing Typedef.tab.h
	rm Typedef.tab.h
	# copying Typedef.tab.c to Typedef.c
	cp Typedef.tab.c Typedef.c
	# removing Typedef.tab.c
	rm -rf Typedef.tab.c
	# compiling Typedef.tab.c
	gcc Typedef.c -o Typedef
	# removing Typedef.c, Typedef.tokens.h and Typedef.lexer.c
	rm -rf Typedef.c Typedef.tokens.h Typedef.lexer.c
	# executing Typedef
	./Typedef


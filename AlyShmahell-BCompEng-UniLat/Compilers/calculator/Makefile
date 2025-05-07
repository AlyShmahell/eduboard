compile: cal.l cal.y
	# calling flex
	flex cal.l
	# copying lex.yy.c to cal.lexer.c
	cp lex.yy.c cal.lexer.c
	# removing lex.yy.c
	rm lex.yy.c
	# calling bison
	bison -d cal.y
	# copying cal.tab.h to cal.tokens.h
	cp cal.tab.h cal.tokens.h
	# removing cal.tab.h
	rm cal.tab.h
	# copying cal.tab.c to cal.c
	cp cal.tab.c cal.c
	# removing cal.tab.c
	rm -rf cal.tab.c
	# compiling cal.tab.c
	gcc cal.c -o cal
	# removing cal.c, cal.tokens.h and cal.lexer.c
	rm -rf cal.c cal.tokens.h cal.lexer.c
	# executing cal
	./cal


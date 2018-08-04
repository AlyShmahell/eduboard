compile: switch.l switch.y
	# calling flex
	flex switch.l
	# copying lex.yy.c to switch.lexer.c
	cp lex.yy.c switch.lexer.c
	# removing lex.yy.c
	rm lex.yy.c
	# calling bison
	bison -d switch.y
	# copying switch.tab.h to switch.tokens.h
	cp switch.tab.h switch.tokens.h
	# removing switch.tab.h
	rm switch.tab.h
	# copying switch.tab.c to switch.c
	cp switch.tab.c switch.c
	# removing switch.tab.c
	rm -rf switch.tab.c
	# compiling switch.tab.c
	gcc switch.c -o switch
	# removing switch.c, switch.tokens.h and switch.lexer.c
	rm -rf switch.c switch.tokens.h switch.lexer.c
	# executing switch
	./switch


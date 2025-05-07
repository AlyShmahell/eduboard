compile: IfThenElse.l IfThenElse.y
	# calling flex
	flex IfThenElse.l
	# copying lex.yy.c to IfThenElse.lexer.c
	cp lex.yy.c IfThenElse.lexer.c
	# removing lex.yy.c
	rm lex.yy.c
	# calling bison
	bison -d IfThenElse.y
	# copying IfThenElse.tab.h to IfThenElse.tokens.h
	cp IfThenElse.tab.h IfThenElse.tokens.h
	# removing IfThenElse.tab.h
	rm IfThenElse.tab.h
	# copying IfThenElse.tab.c to IfThenElse.c
	cp IfThenElse.tab.c IfThenElse.c
	# removing IfThenElse.tab.c
	rm -rf IfThenElse.tab.c
	# compiling IfThenElse.tab.c
	gcc IfThenElse.c -o IfThenElse
	# removing IfThenElse.c, IfThenElse.tokens.h and IfThenElse.lexer.c
	rm -rf IfThenElse.c IfThenElse.tokens.h IfThenElse.lexer.c
	# executing IfThenElse
	./IfThenElse


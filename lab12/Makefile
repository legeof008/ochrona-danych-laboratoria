GCC=gcc
FLAGS=-z execstack -fno-stack-protector
NAME_LOGIN=login
FILES_LOGIN=z1/login.c
NAME_ATM=login
FILES_ATM=z2/login.c

login: $(FILES_LOGIN)
	$(GCC) $(FLAGS) -o $(NAME_LOGIN) $(FILES_LOGIN)

atm: $(FILES_ATM)
	$(GCC) $(FLAGS) -o $(NAME_ATM) $(FILES_ATM)
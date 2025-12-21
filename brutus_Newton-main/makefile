###################################################################
# Paths for M2 Mac with Homebrew
BREW_PREFIX = /opt/homebrew
HOME_DIR = <home>

# mpreal location
MPRLIB = $(HOME_DIR)/src/mpreal

# Include directories
INCLUDE_DIRS = -I$(BREW_PREFIX)/include -I$(MPRLIB)

# Library directories
LIB_DIRS = -L$(BREW_PREFIX)/lib

# Project directories
HOME    = ./
ROOTDIR = ./
LIB     = $(HOME)lib/
MPLIB   = $(HOME)mplib/
DIRTIM  = $(LIB)Timer/
DIRDH   = $(LIB)Data_Handler/

###################################################################
# Compiler settings
COMP = g++
CFLAGS = -O3 -std=c++11 -DMPFR_USE_NO_MACRO -DMPFR_USE_INTMAX_T
CC  = $(COMP) $(CFLAGS) -c
CO  = $(COMP) $(CFLAGS) -o

###################################################################
EXE = brutus
all: $(EXE)

###################################################################
brutus: main.o Brutus.o Bulirsch_Stoer.o Cluster.o Star.o Data_Handler.o Timer.o 
	$(CO) brutus main.o Brutus.o Bulirsch_Stoer.o Cluster.o Star.o Data_Handler.o Timer.o $(LIB_DIRS) -lgmpxx -lgmp -lmpfr

###################################################################
main.o: main.cpp Brutus.o Bulirsch_Stoer.o Cluster.o Star.o Data_Handler.o Timer.o 
	$(CC) main.cpp -I$(DIRTIM) -I$(DIRDH) -I$(MPRLIB) $(INCLUDE_DIRS)

###################################################################
Brutus.o: Brutus.h Brutus.cpp Bulirsch_Stoer.o Cluster.o Star.o Timer.o
	$(CC) Brutus.cpp -I$(DIRTIM) -I$(MPRLIB) $(INCLUDE_DIRS)

Bulirsch_Stoer.o: Bulirsch_Stoer.h Bulirsch_Stoer.cpp Cluster.o Star.o 
	$(CC) Bulirsch_Stoer.cpp -I$(DIRTIM) -I$(MPRLIB) $(INCLUDE_DIRS)

Cluster.o: Cluster.h Cluster.cpp Star.o 
	$(CC) Cluster.cpp -I$(MPRLIB) $(INCLUDE_DIRS)

Star.o: Star.h Star.cpp 
	$(CC) Star.cpp -I$(MPRLIB) $(INCLUDE_DIRS)

Data_Handler.o: $(DIRDH)Data_Handler.h $(DIRDH)Data_Handler.cpp
	$(CC) $(DIRDH)Data_Handler.cpp $(INCLUDE_DIRS)

Timer.o: $(DIRTIM)Timer.h $(DIRTIM)Timer.cpp
	$(CC) $(DIRTIM)Timer.cpp $(INCLUDE_DIRS)

###################################################################
clean:
	rm -f *~
	rm -f *.o
	rm -f -r ccache
	rm -f .fuse*
	rm -f brutus

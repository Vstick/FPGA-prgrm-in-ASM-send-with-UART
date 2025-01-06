# Variables pour l'assemblage
ASM_FILE ?= mon_programme.asm      # Nom du fichier assembleur (par défaut si non fourni)
BIN_FILE = $(ASM_FILE:.asm=.bin)   # Nom du fichier binaire généré
PYTHON = python3                   # Commande Python (ajustez si nécessaire)
ASSEMBLER_SCRIPT = assembler.py    # Script Python pour assembler

# Variables pour le programme C++
CC = g++
CFLAGS = -O3 -Wall -std=c++11
LDFLAGS =
EXEC = main
SRC = ./main.cpp
OBJ = $(SRC:.cpp=.o)

# Règle par défaut
all: $(BIN_FILE) send

# Génération du fichier binaire uniquement
bin: $(BIN_FILE)

# Génération du fichier binaire
$(BIN_FILE): $(ASM_FILE)
	$(PYTHON) $(ASSEMBLER_SCRIPT) $(ASM_FILE) $(BIN_FILE)

# Commande pour compiler le programme C++
compile: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CC) $(CFLAGS) -o $@ -c $<

# Envoi du fichier binaire au FPGA via UART
send: $(BIN_FILE)
	./$(EXEC) $(BIN_FILE)

# Nettoyage des fichiers générés
clean:
	rm -f $(SRC:.cpp=.o) $(EXEC) $(BIN_FILE)

# Aide
help:
	@echo "Commandes disponibles :"
	@echo "  make all ASM_FILE=<nom.asm>          - Assemble et envoie le fichier sur le FPGA via UART."
	@echo "  make bin ASM_FILE=<nom.asm>          - Génère uniquement le fichier binaire spécifié."
	@echo "  make send ASM_FILE=<nom.asm>         - Envoie le fichier binaire au FPGA via UART."
	@echo "  make compile                         - Compile le programme main.cpp en un exécutable."
	@echo "  make clean                           - Supprime les fichiers générés."
	@echo "  make help                            - Affiche cette aide."

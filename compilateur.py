class PICInterpreter:
    def assemble(self, input_file):
        opcode_map = {
            'ADDWF': '000111', 'ANDWF': '000101', 'CLRF': '000001',
            'CLRW': '000001', 'COMF': '001001', 'DECF': '000011',
            'DECFSZ': '001011', 'INCF': '001010', 'INCFSZ': '001111',
            'IORWF': '000100', 'MOVF': '001000', 'MOVWF': '0000001', 
            'NOP': '000000', 'RLF': '001101', 'RRF': '001100', 
            'SUBWF': '000010', 'SWAPF': '001110', 'XORWF': '000110', 
            'BCF': '0100', 'BSF': '0101', 'BTFSC': '0110', 'BTFSS': '0111', 
            'ADDLW': '111110', 'ANDLW': '111001', 'GOTO': '101', 
            'IORLW': '111000', 'MOVLW': '110000', 'SUBLW': '111100', 
            'XORLW': '111010'
        }

        binary_lines = []

        with open(input_file, 'r') as asm_file:
            for line in asm_file:
                # Ignorer les lignes vides ou commentaires
                line = line.strip()
                if not line or line.startswith(';'):
                    continue

                parts = line.split()
                instr = parts[0]
                args = parts[1:] if len(parts) > 1 else []

                if instr not in opcode_map:
                    raise ValueError(f"Instruction inconnue : {instr}")

                opcode = opcode_map[instr]

                # Générer le binaire selon le type d'instruction
                if instr in ['MOVLW', 'GOTO', 'ADDLW', 'SUBLW', 'ANDLW', 'IORLW', 'XORLW']:
                    literal = int(args[0]) if args else 0
                    literal_bin = f"{literal:011b}" if instr == 'GOTO' else f"{literal:08b}"
                    binary_instr = opcode + literal_bin
                elif instr in ['MOVWF', 'CLRF']:
                    f = int(args[0])
                    binary_instr = opcode + f"{f:07b}"
                elif instr in ['ADDWF', 'ANDWF', 'DECF', 'DECFSZ', 'INCF', 'INCFSZ', 'IORWF', 'COMF', 'MOVF', 'RLF', 'RRF', 'SUBWF', 'SWAPF', 'XORWF']:
                    f = int(args[0])  # Registre fichier
                    d = int(args[1]) if len(args) > 1 else 0  # Bit de destination (0 ou 1)
                    # Construire le binaire dans le format `opcode|d|f`
                    binary_instr = opcode + f"{d:01b}" + f"{f:07b}"
                elif instr in ['BCF', 'BSF', 'BTFSC', 'BTFSS']:
                    f = int(args[0])
                    b = int(args[1])
                    binary_instr = opcode + f"{b:03b}" + f"{f:07b}"
                elif instr == 'NOP':
                    binary_instr = '00000000000000'
                elif instr == 'CLRW':
                    binary_instr = '00000100000000'
                else:
                    raise ValueError(f"Format inconnu pour l'instruction : {instr}")

                # Ajouter préfixe '00' pour compléter à 16 bits
                full_binary = '00' + binary_instr

                # Vérification de la longueur
                if len(full_binary) != 16:
                    raise ValueError(f"L'instruction générée n'est pas valide (pas 16 bits) : {full_binary}")

                # Convertir en uint16
                uint16_value = int(full_binary, 2)  # Conversion binaire -> uint16
                binary_lines.append(uint16_value)

        # Retourner toutes les instructions assemblées en uint16
        return binary_lines

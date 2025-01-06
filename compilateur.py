class PICInterpreter:
    def __init__(self):
        self.opcode_map = {
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

        self.symbol_map = {
            "RP0": 5,        # 
            "W": 0,          # Accumulateur W
            "F": 1,          # RAM
            "STATUS": 3,     # Adresse du registre STATUS
            "C": 0,          # Bit Carry (STATUS, bit 0)
            "DC": 1,         # Bit Digit Carry (STATUS, bit 1)
            "Z": 2,          # Bit Zero (STATUS, bit 2)
        }

    def assemble(self, input_file):
        binary_lines = []
        labels = {}
        instructions = []

        # Première passe : identifier les balises
        with open(input_file, 'r') as asm_file:
            address = 0
            for line in asm_file:
                # Supprimer les commentaires
                line = line.split(';')[0].strip()
                if not line:  # Ignorer les lignes vides
                    continue

                if ':' in line:  # Identifier les balises
                    label, instruction = line.split(':', 1)
                    labels[label.strip()] = address
                    if instruction.strip():  # Si une instruction suit la balise
                        instructions.append(instruction.strip())
                        address += 1
                else:
                    instructions.append(line)
                    address += 1

        # Deuxième passe : assembler les instructions
        for line in instructions:
            parts = line.split()
            instr = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            # Nettoyer les arguments (retirer les virgules ou espaces inutiles)
            args = [arg.strip(',') for arg in args]

            if instr not in self.opcode_map:
                raise ValueError(f"Instruction inconnue : {instr}")

            opcode = self.opcode_map[instr]
            resolved_args = []

            # Résolution des arguments (balises, symboles, ou valeurs numériques)
            for arg in args:
                if arg in self.symbol_map:  # Symboles prédéfinis
                    resolved_args.append(self.symbol_map[arg])
                elif arg in labels:  # Balises
                    resolved_args.append(labels[arg])
                else:  # Valeurs numériques (hex, décimal, octal)
                    resolved_args.append(int(arg, 0))

            # Génération des instructions binaires
            if instr in ['MOVLW', 'GOTO', 'ADDLW', 'SUBLW', 'ANDLW', 'IORLW', 'XORLW']:
                literal = resolved_args[0] if resolved_args else 0
                literal_bin = f"{literal:011b}" if instr == 'GOTO' else f"{literal:08b}"
                binary_instr = opcode + literal_bin
            elif instr in ['MOVWF', 'CLRF']:
                f = resolved_args[0]
                binary_instr = opcode + f"{f:07b}"
            elif instr in ['ADDWF', 'ANDWF', 'DECF', 'DECFSZ', 'INCF', 'INCFSZ', 'IORWF', 'COMF', 'MOVF', 'RLF', 'RRF', 'SUBWF', 'SWAPF', 'XORWF']:
                f = resolved_args[0]
                d = resolved_args[1] if len(resolved_args) > 1 else 0
                binary_instr = opcode + f"{d:01b}" + f"{f:07b}"
            elif instr in ['BCF', 'BSF', 'BTFSC', 'BTFSS']:
                f = resolved_args[0]
                b = resolved_args[1]
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
            if len(full_binary) < 16:  # Compléter avec des zéros si nécessaire
                full_binary = full_binary.zfill(16)
            elif len(full_binary) > 16:
                raise ValueError(f"L'instruction générée n'est pas valide (trop longue) : {full_binary}")

            # Convertir en uint16
            uint16_value = int(full_binary, 2)
            binary_lines.append(uint16_value)

        # Retourner toutes les instructions assemblées en uint16
        return binary_lines

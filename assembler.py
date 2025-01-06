import sys
from compilateur import PICInterpreter

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <input.asm> <output.bin>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Initialisation de l'assembleur
    interpreter = PICInterpreter()

    try:
        # Obtenir le contenu binaire sous forme de uint16 (liste d'entiers)
        binary_data = interpreter.assemble(input_file)

        # Écrire le contenu binaire dans le fichier de sortie sous forme binaire
        with open(output_file, "wb") as f:
            for value in binary_data:
                # Convertir chaque uint16 en bytes et l'écrire dans le fichier
                f.write(value.to_bytes(2, byteorder='little'))

        print(f"Le fichier binaire '{output_file}' a été généré avec succès.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{input_file}' est introuvable.")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        sys.exit(1)

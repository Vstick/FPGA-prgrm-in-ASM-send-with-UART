; Division par soustraction répétée
; Divise 0x20 (dividende) par 0x10 (diviseur)
; Résultat : Quotient dans 0x21, Reste dans 0x22

start:
    MOVLW 0x15         ; Charger le dividende (21 en décimal)
    MOVWF 0x20         ; Stocker dans 0x20
    MOVLW 0x03         ; Charger le diviseur (3 en décimal)
    MOVWF 0x10         ; Stocker dans 0x10
    CLRF 0x21          ; Effacer le quotient
    CLRF 0x22          ; Effacer le reste

divide_loop:
    MOVF 0x20, 0       ; Charger le dividende actuel dans WREG
    SUBWF 0x10, W      ; Soustraire le diviseur
    BTFSS STATUS, C    ; Si le résultat est négatif, sortir de la boucle
    GOTO division_done
    MOVF 0x20, W       ; Soustraire le diviseur du dividende
    SUBWF 0x10, F
    INCF 0x21, 1       ; Incrémenter le quotient
    GOTO divide_loop

division_done:
    MOVF 0x20, 0       ; Charger le reste
    MOVWF 0x22         ; Stocker le reste dans 0x22

end:
    NOP                ; Boucle infinie
    GOTO end

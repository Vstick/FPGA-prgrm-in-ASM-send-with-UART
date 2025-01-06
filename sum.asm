; Calcul d'une multiplication
; Valeur à multiplier
MOVLW 2
; Stocker dans le registre 10
MOVWF 10
; Nombre de fois à multiplier
MOVLW 5
; Stocker dans le registre 11
MOVWF 11
; Clear WReg
CLRW
; Ajouter WREG au registre 10 et stocker dans 12
ADDWF 10 0
MOVWF 12
; Décrémenter le registre 11 et sauter si zéro
DECFSZ 11 1
; Aller à l'adresse 5
GOTO 5
; Aller à l'adresse 8
GOTO 9

#classe che descrive i valori ammissibili in una sudoku_grid
class SudokuChars:
    digits = '123456789'
    # Valori che indicano che la cella è vuota
    delimiters = '0.'
    #Valori ammissibili in una cella
    valids = digits + delimiters

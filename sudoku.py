"""Sudoku script by Cristiano Salerno, matricola M63/848
Elaborato scelto dal Powerpoint 'Tracce_elaborato_finale.pptx'
Traccia:
'Implementare una applicazione che genera esercizi di Sudoku e li risolve.'

Ricordiamo brevemente che il Sudoku è un puzzle 9x9 che consiste nel posizionare 81 permutazioni
del vettore (1..9) all'interno di una griglia, e come vincoli abbiamo che un elemento deve essere
unico sulla stessa riga, sulla stessa colonna e nella stessa sottogriglia 3x3.
Chiameremo tali elementi nel corso dello script 'unità', cioé elementi della griglia tali che
contengano una sola ripetizione di ogni cifra.

In questo script indicheremo le colonne con i numeri 1..9 e le righe con le lettere A..I,
e di conseguenza le singole celle con la notazione letteraNumero (es A1 è la casella in alto
a sinistra del sudoku per intero).
"""

# funzione utility per ottenere tutte le coppie di due stringe, prese elemento per elemento
def mix(A, B):
    return [f'{a}{b}' for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
cells = mix(rows, cols)

# memorizzo tutte le unità presenti all'interno della mia griglia 9x9
unitslist = (
    # ottieni tutte le colonne
    [mix(rows, c) for c in cols] +
    # ottieni tutte le righe
    [mix(r, cols) for r in rows] +
    # ottieni tutte le sottogriglie
    [mix(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

# memorizzo in un dizionario le tuple che hanno come chiave tutte le celle della griglia,
# e come valore, per ogni cella, tutte le unità a cui essa appartiene
units = dict(
    (c, [u for u in unitslist if c in u])
    for c in cells)

# memorizzo in un dizionario tutti i pari per ogni cella, cioé tutti gli elementi appartenenti
# alle tre unità di una cella esclusa la cella stessa (es A1 sta sulla stessa riga di Ai (i in 1..9)
# sulla stessa colonna di j1 (j in A..I) e nella stessa sottogriglia A1 A2 A3, B1 B2 B3, C1 C2 C3;
# memorizzerò quindi Ai (i in 2..9), j1 (j in B..I) e A2 A3, B1 B2 B3, C1 C2 C3;
peers = dict(
    (c, set(sum(units[c], [])) - {c}
     for c in cells)
)


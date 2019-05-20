"""Sudoku script by Cristiano Salerno, matricola M63/848
Elaborato scelto dal Powerpoint 'Tracce_elaborato_finale.pptx'
Traccia:
'Implementare una applicazione che genera esercizi di Sudoku e li risolve.'

Ricordiamo brevemente che il Sudoku è un puzzle 9x9 che consiste nel posizionare 81 permutazioni
del vettore (1..9) all'interno di una griglia, e come vincoli abbiamo che un elemento deve essere
unico sulla stessa riga, sulla stessa colonna e nella stessa sottogriglia 3x3.

Variabili decisionali: x(i,j,k)
(i,j) rappresenta la generica cella della nostra griglia,
k rappresenta il valore inserito all'interno di tale cella.

Vincoli:
somma per ogni i,j per k = 1..9 x(i,j,k) = 1 -> ogni cella deve contenere un valore 1..9
somma per ogni i,k per j = 1..9 x(i,j,k) = 1 -> ogni riga deve avere una permutazione di 1..9
somma per ogni j,k per i = 1..9 x(i,j,k) = 1 -> ogni col come sopra
somma per ogni h,k per (i,j) appartenenti al RQ_h x(i,j,k) = 1 -> ogni riquadro come sopra
"""
import random

"""Classi per gestire eccezioni riguardanti il mondo del Sudoku"""
class SudokuError(Exception): pass
class GridError(SudokuError): pass

"""Classi per gestire le entità riguardanti il mondo del Sudoku"""
class GridString(str): pass
class GridValues(dict): pass
class GridCell(str): pass

# utility per mixare velocemente tutti gli elementi di due vettori di stringhe
def mix(A, B):
    return [a + b for a in A for b in B]

digits = '123456789' # insieme dei numeri ammessi in una casella
rows = 'ABCDEFGHI' # insieme delle righe
cols = digits # insieme delle colonne
cells = mix(rows, cols) # insieme delle celle
# vettore delle unità;
# per ogni cella definiamo unità come l'unione di riga, colonna e
# sottogriglia a cui appartiene la cella
unitlist = ([mix(rows, c) for c in cols] +
            [mix(r, cols) for r in rows] +
            [mix(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
# dizionario di cella : unità della cella
units = dict((cell, [u for u in unitlist if cell in u])
             for cell in cells)
# dizionario dei pari; i pari sono tutti gli elementi che stanno
# nell'unità di una cella e non sono la cella stessa
# le regole del sudoku dicono che per ogni cella contenente il valore i
# nessun altro pari deve avere lo stesso valore i
peers = dict((cell, set(sum(units[cell], [])) - {cell})
             for cell in cells)

# funzione per ottenere un dizionario con assegnati ad ogni cella
# il corrispettivo carattere della stringa grid che rappresenta il sudoku
def grid_values(grid: GridString):
    # i caratteri validi sono tutti quelli numerici o al più '.'
    chars = [char for char in grid if char in digits or char in '0.']
    # assicuriamoci che il num di caratteri validi sia 81
    if len(chars) != 81:
        raise GridError('La griglia non ha 81 caratteri validi!')
    # zip crea le tuple cells(i),chars(i), mentre dict
    # crea il dizionario con chiave:cells(i) e valore:chars(i)
    return GridValues(zip(cells, chars))

# funzione per convertire una stringa rappresentante uno schema sudoku
# nel formato 0-9 + '.' (es stringa grid = '1230456.789')
# otteniamo lo schema delle annotazioni
def parse_grid(grid: GridString):
    # creiamo un dizionario al cui interno mettiamo tutti i numeri
    # che rappresentano i numeri possibili appartenenti a quella cella
    values = GridValues((cell, digits) for cell in cells)
    # cicliamo tutte le coppie presenti
    for cell, digit in grid_values(grid).items():
        # se non possiamo assegnare il numero della stringa grid
        # all'interno della cella indicata, alza un'eccezione
        if digit in digits and not assign(values, cell, digit):
            #return False
            raise GridError('La griglia non è valida!')
    return values

# funzione per assegnare il valore NUM alla cella CELL
def assign(values: GridValues, cell: GridCell, num: str):
    # ottieni gli altri valori della cella
    other_digits = values[cell].replace(num, '')
    # prova a eliminare tutti gli altri valori della cella,
    # se anche uno solo mi crea problemi allora non posso assegnare
    # il valore NUM alla cella CELL, cioé se eliminate fallisce
    # anche una sola volta allora non è quella la cifra giusta per quella cella
    for digit in other_digits:
        if not eliminate(values, cell, digit):
            return False
    return values

# funzione di backtracking per provare a eliminare una possibilità da una cella
def eliminate(values: GridValues, cell: GridCell, num: str):
    # se il numero non c'è, già è stato eliminato
    if num not in values[cell]:
        return values
    # cancella preventivamente il numero dalla cella
    values[cell] = values[cell].replace(num, '')
    # se non ho più possibilità nella cella, ho un errore
    if len(values[cell]) == 0:
        return False
    # se mi è rimasta una sola possibilità, applico il backtracking e
    # provo ad eliminare ricorsivamente tutte le istanze di guess da
    # tutti i pari della mia cella
    elif len(values[cell]) == 1:
        guess = values[cell]
        for peer in peers[cell]:
            if not eliminate(values, peer, guess):
                return False
    # se in un'unità abbiamo un unico spazio dove inserire NUM, va messo lì,
    # altrimenti in un'unità non avremmo nessun NUM -> violazione vincoli sudoku
    for unit in units[cell]:
        places = [c for c in unit if num in values[c]]
        # se non c'è nessun posto, errore
        # non posso cancellare num dalla cella perché nessun'altra
        # cella dell'unità può ospitare tale numero
        if len(places) == 0:
            return False
        # se c'è un unico posto, provo ad assegnare il numero a quella casella
        # usando la funzione assign: questo vuol dire che scatenerò di nuovo eliminate
        # ricorsivamente
        # strategia Depth First, esploro sempre più in profondità
        elif len(places) == 1:
            if not assign(values, places[0], num):
                return False
    return values

# funzione per stampare una griglia sudoku 9x9
def print_sudoku(values: GridValues):
    # allarga dinamicamente la larghezza in base al numero di possibilità
    # che ogni casella può avere
    width = 2 + max(len(values[c]) for c in cells)
    # crea una linea fatta da '-' (dinamici) e un + in prossimità delle colonne
    line = '+'.join(['-' * (3*width)] * 3)
    # per ogni riga stampa le possibilità (values[r+c]), centrate, e se
    # la colonna è la 3 o la 6 aggiungi un '|' di separazione dopo
    for r in rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in cols))
        # se r è la terza o sesta riga, stampa dopo la riga dei numeri
        # anche la linea creata prima
        if r in 'CF': print(line)
    print()

# funzione per risolvere una griglia sudoku in formato testuale
def solve(grid: GridString):
    return search(parse_grid(grid))

def some(seq):
    ls = [elem for elem in seq if elem]
    if len(ls) == 0: return False
    else: return ls[0]

def search(values: GridValues):
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in cells):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in cells if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def random_puzzle(n: int = 17):
    if n < 17:
        raise ValueError("n dev'essere maggiore o uguale di 17!")
    values = GridValues((s, digits) for s in cells)
    # creo una copia delle celle
    cells_copy = cells.copy()
    # randomizzo l'ordine delle celle
    # shuffle lavora in place
    random.shuffle(cells_copy)
    # conto quanti elementi ho inserito
    count = 0
    for cell in cells_copy:
        # scelgo il numero in maniera randomica dai possibili valori che può avere
        number = random.choice(values[cell])
        # se non posso assegnare quel numero a quella cella,
        # esco e rifaccio il puzzle random
        if not assign(values, cell, number): break
        # se sono qui, ho assegnato quel numero a quella cella
        count += 1
        # se ho terminato, restituisci la stringa del puzzle
        if count == n:
            return GridString(''.join(values[c] if len(values[c]) == 1 else '.' for c in cells))
    return random_puzzle(n)

grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
hard1 = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
grid_mia = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

if __name__ == '__main__':
    for i in range(20):
        rand_puzzle = random_puzzle(30)
        print_sudoku(grid_values(rand_puzzle))
        print_sudoku(solve(rand_puzzle))
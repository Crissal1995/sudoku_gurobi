from tkinter import *
from tkinter.ttk import *
from tkinter import font
from Model.sudoku_model import SudokuGrid

# classe per gestire la griglia del sudoku
class SudokuFrame(Frame):
    def __init__(self, parent):
        # creazione grafica del frame
        super().__init__(parent, padding = '5 5 5 5')
        self.pack()

        # definizione del sudoku_grid, modello del sudoku
        self.sudoku_grid = SudokuGrid()

        # vettore dei subgrids frame
        self.subgrids = self.make_subgrids()

        # otteniamo le celle (frame) e le celle nella sottogriglia (indici)
        # che ci servono poi dopo nel gurobi_controller
        self.cells, self.sudoku_grid.cells_in_subgrid = self.make_cells()

    def make_subgrids(self):
        subgrids = []
        for i in range(3):
            for j in range(3):
                if j == 2:  # ultima cella della riga
                    padding = '0 0 0 5'
                else:  # prime due celle
                    padding = '0 0 5 5'
                subf = Frame(self, padding=padding)
                subf.grid(row=i, column=j)
                subgrids.append(subf)
        return subgrids

    def make_cells(self):
        cells, cells_in_subgrid = ([],{})
        for i in range(9):
            for j in range(9):
                sub_idx = None
                # assegna la sottogriglia corrispondente alla cella (i,j)
                if i in [0, 1, 2]:  # prima riga
                    if j in [0, 1, 2]: sub_idx = 0
                    elif j in [3, 4, 5]: sub_idx = 1
                    else: sub_idx = 2
                elif i in [3, 4, 5]:  # seconda riga
                    if j in [0, 1, 2]: sub_idx = 3
                    elif j in [3, 4, 5]: sub_idx = 4
                    else: sub_idx = 5
                elif i in [6, 7, 8]:  # terza riga
                    if j in [0, 1, 2]: sub_idx = 6
                    elif j in [3, 4, 5]: sub_idx = 7
                    else: sub_idx = 8
                # assegna la cella al subframe individuato prima
                subgrid = self.subgrids[sub_idx]
                cell = SudokuCell(subgrid, i, j)
                # assegna la cella alla sottogriglia corrispondente
                if subgrid in cells_in_subgrid:
                    cells_in_subgrid[sub_idx].append( (i,j) )
                else:
                    cells_in_subgrid[sub_idx] = [ (i,j) ]
                # posiziona la cella nella sottogriglia
                subrow = i % 3 + i // 3
                subcol = j % 3 + j // 3
                cell.grid(row=subrow, column=subcol)
                # aggiungi la cella al vettore delle ref
                cells.append(cell)
        return cells, cells_in_subgrid

    def load_grid(self, grid: str):
        assert(self.sudoku_grid.is_valid_grid())
        for i in range(81):
            self.cells[i].make_nonstatic()
            digit = grid[i]
            if digit in SudokuGrid.delimiters: digit = ''
            self.cells[i].set_value(digit)
            if digit != '': self.cells[i].make_static()
        # cambiare la griglia inserita
        self.sudoku_grid.set_grid(grid)

class SudokuCell(Frame):
    def __init__(self, parent, row, column, is_static = False):
        super().__init__(parent)
        self.sudoku_font = font.Font(size=17)
        self.row = row
        self.column = column
        self.is_static = is_static
        self.text = StringVar()
        # %P è il parametro della nuova stringa che si ottiene in digitazione
        # https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/entry-validation.html
        val_cmd = (self.register(self.validate_input), '%P')
        self.entry = Entry(self, width = 3, justify = 'center', font = self.sudoku_font,
                           validate = 'key', validatecommand = val_cmd,
                           textvariable = self.text)
        self.entry.pack(ipady = 3)

    # funzione callback per validare l'input ed assicurarci che ogni casella
    # o sia vuota o abbia una sola cifra
    def validate_input(self, new_value):
        if self.is_static: return False
        if new_value == '' or new_value in SudokuGrid.digits:
            if len(new_value) <= 1: return True
            else: return False
        return False

    # funzioni per manipolare il testo all'interno di ogni cella
    def set_value(self, text):
        if self.is_static: return
        self.text.set(text)
    def clear_value(self):
        self.text.set('')

    # funzione per rendere una cella statica o meno;
    # generiamo prima una griglia di celle non statiche e poi, in base
    # al puzzle che abbiamo come input, rendiamo determinate celle statiche
    def make_static(self):
        self.is_static = True
        self.entry['state'] = DISABLED
    def make_nonstatic(self):
        self.is_static = False
        self.entry['state'] = NORMAL

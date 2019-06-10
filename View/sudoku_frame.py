from tkinter import *
from tkinter.ttk import *
from Model.sudoku_grid import SudokuGrid
from View.sudoku_cell import SudokuCell

# classe per gestire la griglia del sudoku
class SudokuFrame(Frame):
    def __init__(self, parent):
        # creazione grafica del frame
        super().__init__(parent, padding = '5 5 5 5')
        self.pack()
        # creiamo un riferimento alla griglia del model
        self.sudoku_grid = SudokuGrid()
        # vettore dei subgrids frame
        self.subgrids = self.make_subgrids()
        # otteniamo le celle (frame) e le celle nella sottogriglia (indici)
        # che ci servono poi dopo nel gurobi_controller
        cells_frame = self.make_cells()
        self.cells = cells_frame

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
        cells = []
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
                # posiziona la cella nella sottogriglia
                subrow = i % 3 + i // 3
                subcol = j % 3 + j // 3
                cell.grid(row=subrow, column=subcol)
                # aggiungi la cella al vettore delle ref
                cells.append(cell)
        return cells

    def load_grid(self, grid: str, first_load = True):
        assert(self.sudoku_grid.is_valid_grid())
        for i in range(81):
            if first_load:
                self.cells[i].make_nonstatic()
            digit = grid[i]
            if digit in SudokuGrid.delimiters: digit = ''
            self.cells[i].set_value(digit)
            if digit != '' and first_load:
                self.cells[i].make_static()
        # cambiare la griglia inserita
        self.sudoku_grid.set_grid(grid)
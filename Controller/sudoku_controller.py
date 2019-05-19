import Model.sudoku_view_model as vmodel
import View.sudoku_view as view
from tkinter import messagebox
from tkinter import Tk

class Controller:
    grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    def __init__(self):
        self.root = Tk()
        self.root.title('GUS - Gurobi Sudoku')
        self.sudoku_grid = vmodel.SudokuGrid(self.root)
        self.load_current_grid() # debug
        self.view_manager = view.ViewManager(self, self.root)
        self.root.mainloop() # ultima istruzione da lanciare

    def load_current_grid(self):
        self.sudoku_grid.load_grid(Controller.grid)

    ######## FUNZIONI CALLBACK (associate ai bottoni nella GUI)
    def generate_sudoku(self):
        nnz = self.view_manager.get_choice()
        assert(17 <= nnz <= 81)
        Controller.grid = Controller.grid[-7:] + Controller.grid[:-7]
        self.load_current_grid()

    def risolve_sudoku(self): pass

    def reset_sudoku(self):
        if messagebox.askokcancel('Reset', 'Vuoi resettare il puzzle?'):
            for c in self.sudoku_grid.cells:
                if not c.is_static: c.clear_value()

if __name__ == '__main__':
    Controller()
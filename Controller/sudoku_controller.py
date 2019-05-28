import Controller.gurobi_controller as gurobi
import Model.sudoku_model as model
from tkinter import messagebox

class Controller:
    def __init__(self):
        # instanziamo il singleton del model
        self.sudoku_grid = model.SudokuGrid()

        # dobbiamo importare dentro l'init per evitare un import circolare
        import View.sudoku_view as view

        # creiamo la gui del programma
        self.view_manager = view.ViewManager(self)

        # creazione controller Gurobi e relativo modello
        self.gurobi_control = gurobi.GurobiController()

        # settiamo una griglia di partenza
        self.load_current_grid()

        # lanciamo l'applicazione
        self.view_manager.start_app()

    @property
    def grid(self):
        return self.sudoku_grid.grid

    def load_current_grid(self, first_load=True):
        self.view_manager.sudoku_frame.load_grid(self.grid, first_load)

    # Funzioni callback associate ai bottoni nella GUI
    def generate_sudoku(self):
        self.gurobi_control.reset_vars()
        nnz = self.view_manager.get_choice()
        assert(17 <= nnz <= 81)
        # TODO GENERAZIONE REALE CON GUROBI
        # debug
        self.sudoku_grid.set_grid(self.grid[-7:] + self.grid[:-7])
        # TODO FINE GENERAZIONE
        self.load_current_grid()

    def risolve_sudoku(self):
        if self.sudoku_grid.full_cells_count == 81:
            return messagebox.showerror('Errore','Il sudoku è già stato risolto!')
        self.gurobi_control.set_vars(self.sudoku_grid.grid)
        try:
            grid_sol = self.gurobi_control.resolve_grid()
        except gurobi.GurobiError:
            return messagebox.showerror('Errore', 'Il sudoku non ha soluzione!')
        self.sudoku_grid.set_grid(grid_sol)
        self.load_current_grid(first_load=False)

    # TODO: CONTROLLARE DEPRECATO
    # Stato: deprecato
    # ---------
    # Motivazione:
    # Non serve cancellare la griglia se non è possibile per l'utente
    # inserire caratteri nelle celle.
    # A meno di non voler creare proprio un gioco Sudoku con inserimento
    # e validazione, ma credo che esuli dalla specifica.
    # def reset_sudoku(self):
    #    if messagebox.askokcancel('Reset', 'Vuoi resettare il puzzle?'):
    #        new_grid = ''
    #        for c in self.view_manager.sudoku_frame.cells:
    #            if not c.is_static:
    #                c.clear_value()
    #                new_grid += '.'
    #            else:
    #                new_grid += self.sudoku_grid.grid[c.row*9 + c.column]
    #        self.sudoku_grid.grid = new_grid
    #        self.load_current_grid()
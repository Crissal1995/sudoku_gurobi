import Controller.gurobi_controller as gurobi
import Model.sudoku_model as model
import random
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

    def start_app(self):
        self.view_manager.start_app()

    def load_current_grid(self, first_load=True):
        self.view_manager.sudoku_frame.load_grid(self.sudoku_grid.grid, first_load)

    # Funzioni callback associate ai bottoni nella GUI
    def generate_sudoku(self):
        nnz = self.view_manager.get_choice()
        assert(17 <= nnz <= 81)
        complete_grid = self.generate_full_grid()
        half_grid = self.generate_half_grid(complete_grid, nnz)

        self.sudoku_grid.set_grid(half_grid)
        self.load_current_grid()

    def risolve_sudoku(self):
        if self.sudoku_grid.full_cells_count_current_grid == 81:
            return messagebox.showerror('Errore','Il sudoku è già stato risolto!')
        try:
            grid_sol = self.gurobi_control.resolve_grid_from_str(self.sudoku_grid.grid)
        except gurobi.GurobiError:
            return messagebox.showerror('Errore', 'Il sudoku non ha soluzione!')

        self.sudoku_grid.set_grid(grid_sol)
        self.load_current_grid(first_load=False)

    def generate_full_grid(self):
        numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.seed()
        random.shuffle(numberList)
        seed = '0' * 81
        # fissiamo i quattro angoli
        for row in [0, 8]:
            for col in [0, 8]:
                element = random.choice(numberList)
                seed = seed[:row*9 + col] + str(element) + seed[row*9 + col + 1:]
                numberList.remove(element)
        # fissiamo i rimanenti numeri
        for element in numberList:
            row = random.randint(1,7)
            col = random.randint(1,7)
            seed = seed[:row*9+col] + str(element) + seed[row*9+col + 1:]
        # ritorniamo la stringa soluzione di gurobi
        return self.gurobi_control.resolve_grid_from_str(grid=seed)

    def generate_half_grid(self, complete_grid, nnz):
        # copia la griglia e lavora su di essa
        half_grid = complete_grid
        # ottieni gli indici delle celle piene
        idxs_full_cells = self.sudoku_grid.full_cells_list(half_grid)
        # mischia questi indici
        random.shuffle(idxs_full_cells)
        # itera fin quando non raggiungi il nnz desiderato
        while self.sudoku_grid.full_cells_count(half_grid) > nnz:
            pos = random.choice(idxs_full_cells)
            # rimuovo la posizione sia se metto '0' (vuota)
            # sia se non posso rimuoverla a causa di GurobiError
            idxs_full_cells.remove(pos)
            # salvo l'elem corrente in caso di eccezione
            old_elem = half_grid[pos]
            # rimuovo l'elem dalla griglia
            half_grid = half_grid[:pos] + '0' + half_grid[pos+1:]
            try:
                self.gurobi_control.resolve_grid_from_str(half_grid)
            except gurobi.GurobiError:
                half_grid = half_grid[:pos] + old_elem + half_grid[pos+1:]
        return half_grid
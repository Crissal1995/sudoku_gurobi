from tkinter import *
from tkinter.ttk import *
import Controller.sudoku_controller as ctr
import View.sudoku_frame as model
from tkinter import messagebox

class ViewManager:
    def __init__(self, controller: ctr.Controller):
        ### inizializzazione gui
        self.root = Tk()
        self.root.title('GUS - Gurobi Sudoku')
        # creiamo la griglia del sudoku
        self.sudoku_frame = model.SudokuFrame(self.root)

        ### frame per contenere label e slider delle celle piene
        self.nnz_frame = Frame(self.root, padding = '5 5 5 5')
        self.nnz_frame.pack()

        # label per indicare il num di caselle piene scelto
        self.nnz_label = Label(self.nnz_frame, text='Numero di celle piene: 17', justify=CENTER)
        self.nnz_label.grid(row=0, column=0, sticky=(W, E))

        # variabile contenente il valore dello slider
        self.nnz = IntVar()
        self.nnz.set(17)

        # slider per decidere un numero in un range fissato
        self.nnz_scale = Scale(self.nnz_frame, from_=17, to=60, orient=HORIZONTAL,
                               variable=self.nnz, command=self.edit_label)
        self.nnz_scale.grid(row=1, column=0, sticky=(W, E))

        ### frame per contenere i bottoni
        self.buttons_frame = Frame(self.root, padding='5 5 5 5')
        self.buttons_frame.pack()

        # bottone per generare un puzzle random
        self.gen_button = Button(self.buttons_frame, text='Genera puzzle',
                                 command=controller.generate_sudoku)
        self.gen_button.grid(row=0, column=0, sticky=(W, E))

        # bottone per risolvere il puzzle corrente
        self.risolve_button = Button(self.buttons_frame, text='Risolvi puzzle',
                                     command=controller.risolve_sudoku)
        self.risolve_button.grid(row=0, column=1, sticky=(W, E))

        # progressbar per il caricamento in fase di generazione
        self.progress_bar = Progressbar(self.nnz_frame, mode = 'determinate',
                                        orient = HORIZONTAL, length = 200)

    def get_choice(self):
        return self.nnz.get()

    def start_app(self):
        self.root.mainloop()

    def load_grid(self, grid: str):
        self.sudoku_frame.load_grid(grid)

    # funzione chiamata ogni volta che lo slider si ferma
    def edit_label(self, _):
        self.nnz_label.configure(text=f'Numero di celle piene: {self.get_choice()}')

    @staticmethod
    def display_warning(message: str):
        return messagebox.showwarning('Attenzione', message)
    @staticmethod
    def display_error(message: str):
        return messagebox.showerror('Errore', message)

    def display_progressbar(self, max_value: int):
        # rimuovi dalla griglia gli elem nnz
        self.nnz_label.grid_remove()
        self.nnz_scale.grid_remove()
        # setta il max
        self.progress_bar['maximum'] = max_value
        # rendi visibile la progress bar
        self.progress_bar.grid(row=0, column=0, sticky=(W,E,N,S))

    def remove_progressbar(self):
        # rimuovi dal frame la progress bar
        self.progress_bar.grid_remove()
        # e rendi di nuovo visibili gli elem nnz
        self.nnz_label.grid(row=0, column=0, sticky=(W,E))
        self.nnz_scale.grid(row=1, column=0, sticky=(W,E))

    def increment_progressbar(self):
        # incrementa il valore della progress bar
        self.progress_bar.step()
        # e aggiorna gli elementi grafici
        self.root.update()

from tkinter import *
from tkinter.ttk import *
import Controller.sudoku_controller as ctr
import View.sudoku_frame as model

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

        # TODO: CONTROLLARE DEPRECATO
        # Stato: deprecato
        # ---------
        # Motivazione:
        # Non serve cancellare la griglia se non è possibile per l'utente
        # inserire caratteri nelle celle.
        # A meno di non voler creare proprio un gioco Sudoku con inserimento
        # e validazione, ma credo che esuli dalla specifica.
        # bottone per resettare il puzzle corrente
        # self.reset_button = Button(self.buttons_frame, text='Resetta puzzle',
        #                           command=controller.reset_sudoku)
        # self.reset_button.grid(row=1, column=0, columnspan=2, sticky=(W, E))

    def get_choice(self):
        return self.nnz.get()

    def start_app(self):
        self.root.mainloop()

    def load_grid(self, grid: str):
        self.sudoku_frame.load_grid(grid)

    # funzione chiamata ogni volta che lo slider si ferma
    def edit_label(self, _):
        self.nnz_label.configure(text=f'Numero di celle piene: {self.get_choice()}')
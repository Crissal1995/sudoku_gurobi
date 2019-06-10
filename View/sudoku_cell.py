from tkinter import *
from tkinter.ttk import *
from tkinter import font

class SudokuCell(Frame):
    def __init__(self, parent, row, column, is_static = False):
        super().__init__(parent)
        self.sudoku_font = font.Font(size=17)
        self.row = row
        self.column = column
        self.is_static = is_static
        self.text = StringVar()
        val_cmd = (self.register(self.validate_input))
        self.entry = Entry(self, width = 3, justify = 'center', font = self.sudoku_font,
                           validate = 'all', validatecommand = val_cmd,
                           textvariable = self.text)
        self.entry.pack(ipady = 3)

    # funzione callback per non permettere l'inserimento dell'utente
    # solo generazione e risolutore sudoku
    @staticmethod
    def validate_input():
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

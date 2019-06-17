from Controller.sudoku_solver_interface import ISudokuSolver
import Model.sudoku_exceptions as error
try:
    import Controller.solver.gurobi_controller as gurobi
except ImportError:
    gurobi = None
try:
    import Controller.solver.mip_controller as mip
except ImportError:
    mip = None


class SolverController:
    __instance = None

    def __new__(cls):
        if SolverController.__instance is None:
            SolverController.__instance = object.__new__(cls)
        return SolverController.__instance

    def __init__(self):
        self._solvers = dict()
        self._solver = None
        self._solver_name = None

        if gurobi:
            self._solvers['gurobi'] = gurobi.GurobiController()
        if mip:
            self._solvers['mip'] = mip.MipController()
        if not self._solvers:  # controlliamo che il dict non sia vuoto
            raise error.SolverNotExistingError('Installare almeno un risolutore '
                                               'compatibile col progetto!')
        for solver in self._solvers.values():
            if not isinstance(solver, ISudokuSolver):
                raise error.SolverNotStandardError('Il solver selezionato non è compatibile con '
                                                   'l\'interfaccia richiesta')

    def get_solver(self):
        if not self._solver:
            key = self._get_solvers()[0]
            self._solver_name = key
            self._solver = self.get_solver_byname(key)
            self._solver._make_model()
        return self._solver

    def get_solver_byname(self, name: str):
        if name in self._solvers:
            return self._solvers[name]
        else:
            raise error.SolverNotExistingError('Il solver selezionato non è presente nel progetto!')

    def _get_solvers(self):
        return list(self._solvers.keys())

    def _del_solver(self, name):
        if name in self._solvers:
            return self._solvers.pop(name)
        else:
            raise error.SolverNotExistingError('Non è possibile cancellare un solver '
                                               'non presente nel progetto!')

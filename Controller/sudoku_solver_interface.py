class ISudokuSolver:
    def _make_model(self):
        raise NotImplementedError

    def resolve_grid(self, grid: str):
        raise NotImplementedError

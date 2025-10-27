from . import Grid, Solver
import random
import numpy as np

class Generator:
    def __init__(self, template_grid: Grid | None = None, seed: int = None):
        # template_grid is assumed to be a fully solved valid Sudoku grid
        if template_grid is not None:
            assert len(template_grid.find_empties()) == 0, "Template grid must be fully solved."
        else:
            template_grid = self.generate_full_board(seed=seed)
        self.template_grid = template_grid

    @staticmethod
    def generate_full_board(seed: int = None) -> Grid:
        """Generate a complete valid Sudoku board using backtracking with MRV.
        """
        random.seed(seed)
        # Use solver to generate a full board
        board = Grid(np.zeros((9, 9), dtype=int))
        solver = Solver(board)
        if not solver.solve(random_bool=True, seed=seed):
            raise RuntimeError("Failed to generate a full Sudoku board")
        return board

    def generate(self, difficulty: int, seed: int = None) -> Grid:
        """Generate a Sudoku puzzle by removing numbers from the template grid.
        
        Args:
            difficulty (int): Number of cells to remove (make empty).
            seed (int, optional): Seed for random number generator for reproducibility. Defaults to None.
        """
        if seed is not None:
            random.seed(seed)
        
        puzzle_grid = Grid(self.template_grid.grid.copy())
        all_positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_positions)
        
        removed = 0
        for row, col in all_positions:
            if removed >= difficulty:
                break
            if puzzle_grid[row, col] != puzzle_grid.unknown:
                puzzle_grid.reset_cell(row, col, force=True)
                removed += 1
        
        return puzzle_grid


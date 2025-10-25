from . import Grid
import random

class Generator:
    def __init__(self, template_grid: Grid):
        # template_grid is assumed to be a fully solved valid Sudoku grid
        assert len(template_grid.find_empties()) == 0, "Template grid must be fully solved."
        self.template_grid = template_grid

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


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
        self.template_grid:Grid = template_grid
        # Initialize all cells as known in the template grid
        for r in range(9):
            for c in range(9):
                self.template_grid._known_cells[r, c] = True

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

    def generate(self, difficulty: int, seed: int = None, ensure_unique: bool = False) -> Grid:
        """Generate a Sudoku puzzle by removing numbers from the template grid.
        
        Ensures the puzzle has exactly one unique solution by verifying after each removal.
        
        Args:
            difficulty (int): Target number of cells to remove (make empty).
            seed (int, optional): Seed for random number generator for reproducibility.
            ensure_unique (bool): If True, verify each removal maintains exactly one solution.
        
        Returns:
            Grid: A Sudoku puzzle with the requested difficulty (or as close as possible
                  while maintaining uniqueness).
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
            
            if puzzle_grid[row, col] == puzzle_grid.unknown:
                continue  # Already empty
            
            # Save the current value before removing
            saved_value = puzzle_grid[row, col]
            
            # Try removing this cell
            puzzle_grid.reset_cell(row, col, force=True)
            puzzle_grid._known_cells[row, col] = False
            
            if ensure_unique:
                # Verify that the puzzle still has exactly one solution
                temp_grid = Grid(puzzle_grid._grid.copy())
                solver = Solver(temp_grid)
                solution_count = solver.solve(max_count=2)
                
                if solution_count == 1:
                    # Exactly one solution - keep the removal
                    removed += 1
                else:
                    # Zero or multiple solutions - revert the change
                    puzzle_grid[row, col] = saved_value
                    puzzle_grid._known_cells[row, col] = True
            else:
                # No uniqueness check - just remove
                removed += 1
        
        return puzzle_grid


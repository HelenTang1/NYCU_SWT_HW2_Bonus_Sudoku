from . import Grid
from collections import deque

class Solver:
    def __init__(self, grid: Grid):
        self.grid:Grid = grid
        self.history = deque(maxlen=grid.size * grid.size)

    def solve(self) -> bool:
        """Perform a single step in solving the Sudoku puzzle using backtracking.
        Returns:
            bool: True if a step was made, False if no step could be made.
        """
        # Find the all empty cells
        empties = self.grid.find_empties()
        if not empties:
            return True  # Puzzle solved
        row, col = empties[0]

        for num in range(1, 10):
            if self.grid.isValidMove(row, col, num):
                self.grid[row, col] = num
                self.history.append((row, col, num))
                if self.solve():
                    return True
                # Backtrack
                self.grid.reset_cell(row, col)
                self.history.pop()
        return False # No solution found

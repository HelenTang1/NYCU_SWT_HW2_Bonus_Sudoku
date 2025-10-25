from . import Grid
from collections import deque

class Solver:
    def __init__(self, grid: Grid):
        self.grid:Grid = grid
        self.empties = deque(self.grid.find_empties())
        self.history = deque(maxlen=len(self.empties))

    def solve(self) -> bool:
        """Solve the Sudoku puzzle using iterative backtracking.
        
        Uses self.history as an explicit stack to avoid recursion, making it 
        more efficient and avoiding potential stack overflow on difficult puzzles.
        Uses self.empties deque as a queue to track remaining empty cells.
        
        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
        if not self.empties:
            return True  # Already solved
        
        # Clear history and use it as our backtracking stack
        # Each entry: (row, col, value)
        self.history.clear()
        
        while self.empties:
            # Get the next empty cell from the front of the queue
            row, col = self.empties[0]
            current_val = self.grid[row, col]
            
            # Determine which number to start trying from
            if current_val != self.grid.unknown:
                # We're backtracking to this cell, try the next number
                start_num = current_val + 1
                self.grid.reset_cell(row, col)
            else:
                # First time visiting this cell
                start_num = 1
            
            # Try numbers from start_num to 9
            found = False
            for num in range(start_num, 10):
                val_move, reason = self.grid.isValidMove(row, col, num)
                if val_move:
                    # Place the number
                    self.grid[row, col] = num
                    self.history.append((row, col, num))
                    # Remove this cell from empties and move forward
                    self.empties.popleft()
                    found = True
                    break
            
            if not found:
                # No valid number found for this cell, need to backtrack
                if not self.history:
                    return False  # No solution exists
                
                # Pop the last placed value
                prev_row, prev_col, prev_num = self.history.pop()
                
                # Add both cells back: current cell stays at front, previous cell goes before it
                self.empties.appendleft((prev_row, prev_col))
        
        return True  # All empties filled successfully
        
            
        

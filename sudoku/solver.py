from . import Grid
from collections import deque
import random

class Solver:
    def __init__(self, grid: Grid):
        self.grid:Grid = grid
        self.empties = deque(self.grid.find_empties())
        self.history = deque(maxlen=len(self.empties))
        self.start_num = {}

    def solve(self, random_bool: bool = False, seed: int | None = None, max_count: int = 1) -> bool:
        """Solve the Sudoku puzzle using iterative backtracking.
        
        Uses self.history as an explicit stack to avoid recursion, making it 
        more efficient and avoiding potential stack overflow on difficult puzzles.
        Uses self.empties deque as a queue to track remaining empty cells.
        
        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
        if not self.empties:
            return 1  # Already solved
        
        # Clear history and use it as our backtracking stack
        # Each entry: (row, col, value)
        self.history.clear()
        random.seed(seed)

        solution_count = 0
        while self.empties or self.history:
            # If we found enough solutions, stop
            if solution_count >= max_count:
                break
            if not self.empties:
                # Found a complete solution
                solution_count += 1
                
                # Force backtrack to find more solutions
                if not self.history:
                    break
                
                prev_row, prev_col, prev_num = self.history.pop()
                self.empties.appendleft((prev_row, prev_col))
                continue

            # Get the next empty cell from the front of the queue
            row, col = self.empties[0]
            current_val = self.grid[row, col]
            
            # Determine which number to start trying from
            if current_val != self.grid.unknown:
                # We're backtracking to this cell, try the next number
                rotated = list(range(self.start_num[(row, col)], 10)) + list(range(1, self.start_num[(row, col)]))
                to_try = rotated[rotated.index(current_val)+1:]  # Try numbers after current_val
                self.grid.reset_cell(row, col)

            else:
                # First time visiting this cell
                if (random_bool):
                    start_num = random.randint(1, 9)
                else:
                    start_num = 1
                self.start_num[(row, col)] = start_num
                # Try numbers in a rotated order starting at `start_num` and wrapping to
                to_try = list(range(start_num, 10)) + list(range(1, self.start_num.get((row, col), 1)))
            
            found = False
            for num in to_try:
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
                    break  # No solution exists
                
                # Pop the last placed value
                prev_row, prev_col, prev_num = self.history.pop()
                # Add both cells back: current cell stays at front, previous cell goes before it
                self.empties.appendleft((prev_row, prev_col))
        
        return solution_count  # All empties filled successfully

    # def solve(self, random_bool: bool = False, seed: int | None = None) -> bool:
    #     """Solve the Sudoku puzzle using iterative backtracking.
        
    #     Uses self.history as an explicit stack to avoid recursion, making it 
    #     more efficient and avoiding potential stack overflow on difficult puzzles.
    #     Uses self.empties deque as a queue to track remaining empty cells.
        
    #     Returns:
    #         bool: True if the puzzle is solved, False otherwise.
    #     """
    #     if not self.empties:
    #         return True  # Already solved
        
    #     # Clear history and use it as our backtracking stack
    #     # Each entry: (row, col, value)
    #     self.history.clear()
    #     random.seed(seed)

        
    #     while self.empties:
    #         # Get the next empty cell from the front of the queue
    #         row, col = self.empties[0]
    #         current_val = self.grid[row, col]
            
    #         # Determine which number to start trying from
    #         if current_val != self.grid.unknown:
    #             # We're backtracking to this cell, try the next number
    #             rotated = list(range(self.start_num[(row, col)], 10)) + list(range(1, self.start_num[(row, col)]))
    #             to_try = rotated[rotated.index(current_val)+1:]  # Try numbers after current_val
    #             self.grid.reset_cell(row, col)

    #         else:
    #             # First time visiting this cell
    #             if (random_bool):
    #                 start_num = random.randint(1, 9)
    #             else:
    #                 start_num = 1
    #             self.start_num[(row, col)] = start_num
    #             # Try numbers in a rotated order starting at `start_num` and wrapping to
    #             to_try = list(range(start_num, 10)) + list(range(1, self.start_num.get((row, col), 1)))
            
    #         found = False
    #         for num in to_try:
    #             val_move, reason = self.grid.isValidMove(row, col, num)
    #             if val_move:
    #                 # Place the number
    #                 self.grid[row, col] = num
    #                 self.history.append((row, col, num))
    #                 # Remove this cell from empties and move forward
    #                 self.empties.popleft()
    #                 found = True
    #                 break
            
    #         if not found:
    #             # No valid number found for this cell, need to backtrack
    #             if not self.history:
    #                 return False  # No solution exists
                
    #             # Pop the last placed value
    #             prev_row, prev_col, prev_num = self.history.pop()
    #             # Add both cells back: current cell stays at front, previous cell goes before it
    #             self.empties.appendleft((prev_row, prev_col))
        
    #     return True  # All empties filled successfully
        
    # def count_solutions(self, max_count: int = 2) -> int:
    #     """Count the number of solutions for the Sudoku puzzle using iterative backtracking.
        
    #     Reuses the same iterative approach as solve() but continues searching after
    #     finding each solution instead of stopping at the first one.
        
    #     Args:
    #         max_count (int): Stop counting after finding this many solutions (default 2).
    #                         This optimization allows early termination when checking uniqueness.
        
    #     Returns:
    #         int: Number of solutions found (capped at max_count).
    #     """
    #     # Save original grid state
    #     original_grid = self.grid.grid.copy()
    #     empties_list = self.grid.find_empties()
        
    #     if not empties_list:
    #         # Grid is already complete - check if it's valid
    #         return 1 if self.grid.isValidGrid() else 0
        
    #     # Reset solver state
    #     self.empties = deque(empties_list)
    #     self.history.clear()
    #     self.start_num = {}
        
    #     solution_count = 0
        
    #     while self.empties or self.history:
    #         # If we found enough solutions, stop
    #         if solution_count >= max_count:
    #             break
            
    #         if not self.empties:
    #             # Found a complete solution
    #             solution_count += 1
                
    #             # Force backtrack to find more solutions
    #             if not self.history:
    #                 break
                
    #             prev_row, prev_col, prev_num = self.history.pop()
    #             self.empties.appendleft((prev_row, prev_col))
    #             continue
            
    #         # Get the next empty cell from the front of the queue
    #         row, col = self.empties[0]
    #         current_val = self.grid._grid[row, col]
            
    #         # Determine which numbers to try
    #         if current_val != self.grid.unknown:
    #             # We're backtracking to this cell, try the next number
    #             rotated = list(range(self.start_num[(row, col)], 10)) + list(range(1, self.start_num[(row, col)]))
    #             to_try = rotated[rotated.index(current_val)+1:]
    #             self.grid._grid[row, col] = self.grid.unknown
    #         else:
    #             # First time visiting this cell
    #             start_num = 1
    #             self.start_num[(row, col)] = start_num
    #             to_try = list(range(start_num, 10)) + list(range(1, self.start_num.get((row, col), 1)))
            
    #         found = False
    #         for num in to_try:
    #             val_move, reason = self.grid.isValidMove(row, col, num)
    #             if val_move:
    #                 # Place the number
    #                 self.grid._grid[row, col] = num
    #                 self.history.append((row, col, num))
    #                 # Remove this cell from empties and move forward
    #                 self.empties.popleft()
    #                 found = True
    #                 break
            
    #         if not found:
    #             # No valid number found for this cell, need to backtrack
    #             if not self.history:
    #                 break  # No more solutions exist
                
    #             # Pop the last placed value
    #             prev_row, prev_col, prev_num = self.history.pop()
    #             # Add previous cell back to retry
    #             self.empties.appendleft((prev_row, prev_col))
        
    #     # Restore original grid state
    #     self.grid._grid[:] = original_grid
    #     self.empties = deque(empties_list)
    #     self.history.clear()
    #     self.start_num = {}
        
    #     return solution_count
        

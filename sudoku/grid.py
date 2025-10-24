import numpy as np

class Grid:
    size:int = 9
    """A class representing a Sudoku grid."""
    def __init__(self, grid: np.ndarray, unknown: int = 0):
        """Initialize the Sudoku grid.
        Args:
            grid (np.ndarray): A 9x9 numpy array representing the Sudoku grid.
            unknown (int): The value representing unknown (empty) cells (default: 0).
        """
        self._grid = np.array(grid, dtype=int)
        self._unknown = unknown
        # Track which cells are known (original values that cannot be changed)
        self._known_cells = (self._grid != unknown)
        
        # Validate the initial grid
        if not self.isValidGrid():
            raise ValueError("Invalid Sudoku grid provided")

    @property
    def grid(self) -> np.ndarray:
        """Get the current grid state."""
        return self._grid.copy()
    
    @property
    def unknown(self) -> int:
        """Get the value representing unknown cells."""
        return self._unknown

    def set_cell(self, row: int, col: int, value: int) -> None:
        """Set a cell value in the grid.
        
        Args:
            row (int): Row index (0-8)
            col (int): Column index (0-8)
            value (int): Value to set (0-9, where 0 typically means unknown)
            
        Raises:
            ValueError: If trying to overwrite a known (original) value
            IndexError: If row or col is out of bounds
        """
        if self.value == self._unknown:
            raise ValueError("Cannot set a cell to the unknown value. Use reset_cell instead.")
        if not (0 <= row < 9 and 0 <= col < 9):
            raise IndexError(f"Cell position ({row}, {col}) is out of bounds")
        
        if self._known_cells[row, col]:
            raise ValueError(f"Cannot overwrite known value at position ({row}, {col})")
        
        if not self.isValidMove(row, col, value):
            raise ValueError(f"Placing value {value} at position ({row}, {col}) is not a valid move")

        self._grid[row, col] = value

    def __setitem__(self, key, value):
        """Allow grid[row, col] = value syntax.
        
        Args:
            key: Tuple of (row, col) indices
            value: Value to set
        """
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            self.set_cell(row, col, value)
        else:
            raise TypeError("Grid indices must be a tuple of (row, col)")

    def __getitem__(self, key):
        """Allow grid[row, col] syntax for getting values.
        
        Args:
            key: Tuple of (row, col) indices
            
        Returns:
            int: Value at the specified position
        """
        if isinstance(key, tuple) and len(key) == 2:
            row, col = key
            if not (0 <= row < 9 and 0 <= col < 9):
                raise IndexError(f"Cell position ({row}, {col}) is out of bounds")
            return self._grid[row, col]
        else:
            raise TypeError("Grid indices must be a tuple of (row, col)")

    def isValidGrid(self) -> bool:
        """Check if the Sudoku grid is valid.
        
        Validates that:
        - No duplicate non-unknown values in any row
        - No duplicate non-unknown values in any column
        - No duplicate non-unknown values in any 3x3 subgrid

        Returns:
            bool: True if the grid is valid, False otherwise.
        """
        for i in range(9):
            row_vals = [v for v in self._grid[i, :] if v != self._unknown]
            if len(row_vals) != len(set(row_vals)):
                return False
            
            col_vals = [v for v in self._grid[:, i] if v != self._unknown]
            if len(col_vals) != len(set(col_vals)):
                return False

            # Check 3x3 subgrid
            subgrid_row = (i // 3) * 3
            subgrid_col = (i % 3) * 3
            subgrid_vals = [v for v in self._grid[subgrid_row:subgrid_row+3, subgrid_col:subgrid_col+3].flatten() if v != self._unknown]
            if len(subgrid_vals) != len(set(subgrid_vals)):
                return False

        return True

    def isValidMove(self, row: int, col: int, value: int) -> bool:
        """Check if placing a value at (row, col) is valid.
        
        Args:
            row (int): Row index (0-8)
            col (int): Column index (0-8)
            value (int): Value to place (1-9)

        Returns:
            bool: True if the placement is valid, False otherwise.
        """
        # You cannot place the unknown value
        if value == self._unknown:
            return False
        
        # You cannot place a value in a known cell
        if self._known_cells[row, col]:
            return False
        
        # Check row
        if value in self._grid[row, :]:
            return False
        
        # Check column
        if value in self._grid[:, col]:
            return False
        
        # Check 3x3 subgrid
        subgrid_row = (row // 3) * 3
        subgrid_col = (col // 3) * 3
        if value in self._grid[subgrid_row:subgrid_row+3, subgrid_col:subgrid_col+3]:
            return False
        
        return True

    def reset_cell(self, row: int, col: int) -> None:
        """Reset a cell to unknown value.
        
        Args:
            row (int): Row index (0-8)
            col (int): Column index (0-8)
            
        Raises:
            ValueError: If trying to reset a known (original) value
            IndexError: If row or col is out of bounds
        """
        if not (0 <= row < 9 and 0 <= col < 9):
            raise IndexError(f"Cell position ({row}, {col}) is out of bounds")
        
        if self._known_cells[row, col]:
            raise ValueError(f"Cannot reset known value at position ({row}, {col})")
        
        self._grid[row, col] = self._unknown

    def find_empties(self) -> list[tuple[int, int]]:
        """Find all empty cells in the grid.
        
        Returns:
            list of tuples: List of (row, col) indices of empty cells.
        """
        empties = []
        for i in range(9):
            for j in range(9):
                if self._grid[i, j] == self._unknown:
                    empties.append((i, j))
        return empties


    def __str__(self) -> str:
        """String representation of the Sudoku grid."""
        lines = []
        for i in range(9):
            if i % 3 == 0 and i != 0:
                lines.append("-" * 21)
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                val = self._grid[i, j]
                row_str += (str(val) if val != self._unknown else ".") + " "
            lines.append(row_str.rstrip())
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """Representation of the Grid object."""
        return f"Grid(shape={self._grid.shape}, unknown={self._unknown})"
    
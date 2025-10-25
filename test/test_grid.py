import sys
sys.path.append(".")
import pytest
import numpy as np
from sudoku import Grid

def test_isValidGrid_valid(a_valid_grid):
    assert a_valid_grid.isValidGrid() == True

@pytest.mark.parametrize(
    "grid_data",
    [
        (
            np.array([
                [5, 3, 0, 0, 7, 0, 0, 3, 0],  # Duplicate '3' in row
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ])
        ),
        (
            np.array([
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [5, 9, 8, 0, 0, 0, 0, 6, 0],  # Duplicate '5' in column
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ])
        ),
        (
            np.array([
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 2, 0, 1, 9, 5, 0, 0, 0], 
                [0, 9, 5, 0, 0, 0, 0, 6, 0],  # Duplicate '5' in top-left subgrid
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ])
        )
    ],
    ids=["invalid row", "invalid column", "invalid subgrid"]
)
def test_isValidGrid_invalid(grid_data):
    with pytest.raises(ValueError):
        Grid(grid_data, unknown=0)

@pytest.mark.parametrize(
    "row, col, value, expected", 
    [
     (0, 2, 4, True),                 # valid move
     (0, 6, 5, False),                # invalid move - row conflict
     (2, 3, 1, False),                # invalid move - column conflict
     (7, 6, 8, False)                 # invalid move - subgrid conflict
    ],
    ids = ["valid move", 
           "invalid row conflict", 
           "invalid column conflict",
           "invalid subgrid conflict"]
)
def test_isValidMove(a_valid_grid, row, col, value, expected):
    val_move, reason = a_valid_grid.isValidMove(row, col, value)
    assert val_move == expected

def test_find_empties(a_valid_grid):
    empty_cells = a_valid_grid.find_empties()
    assert empty_cells == [
        (0, 2), (0, 3), (0, 5), (0, 6), (0, 7), (0, 8),
        (1, 1), (1, 2), (1, 6), (1, 7), (1, 8),
        (2, 0), (2, 3), (2, 4), (2, 5), (2, 6), (2, 8),
        (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), (3, 7),
        (4, 1), (4, 2), (4, 4), (4, 6), (4, 7),
        (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (5, 7),
        (6, 0), (6, 2), (6, 3), (6, 4), (6, 5), (6, 8),
        (7, 0), (7, 1), (7, 2), (7, 6), (7, 7),
        (8, 0), (8, 1), (8, 2), (8, 3), (8, 5), (8, 6)
    ]

def test_reset_cell(a_valid_grid):
    # set an empty cell
    a_valid_grid[0, 2] = 4
    assert a_valid_grid[0, 2] == 4
    # Reset an empty cell
    a_valid_grid.reset_cell(0, 2)
    assert a_valid_grid[0, 2] == 0

    # Try to reset a known cell
    with pytest.raises(ValueError):
        a_valid_grid.reset_cell(0, 0)

    # Try to reset an out-of-bounds cell
    with pytest.raises(IndexError):
        a_valid_grid.reset_cell(9, 0)

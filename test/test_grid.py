import sys
sys.path.append(".")
import pytest
import numpy as np
from sudoku import Grid

@pytest.fixture
def a_valid_grid() -> Grid:
    return Grid(np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]), unknown=0)

def test_isValidGrid_valid(a_valid_grid):
    assert a_valid_grid.isValidGrid() == True

def test_isValidGrid_invalid_row():
    with pytest.raises(ValueError):
        Grid(np.array([
            [5, 3, 0, 0, 7, 0, 0, 3, 0],  # Duplicate '3' in row
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]), unknown=0)

def test_isValidGrid_invalid_column():
    with pytest.raises(ValueError):
        Grid(np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [5, 9, 8, 0, 0, 0, 0, 6, 0],  # Duplicate '5' in column
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]), unknown=0)

def test_isValidGrid_invalid_subgrid():
    with pytest.raises(ValueError):
        Grid(np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 5, 0, 1, 9, 5, 0, 0, 0],  # Duplicate '5' in top-left subgrid
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]), unknown=0)

@pytest.mark.parametrize(
    "row, col, value, expected", 
    [
     (0, 2, 4, True),                 # valid move
     (0, 6, 5, False),                # invalid move - row conflict
     (2, 3, 1, False),                # invalid move - column conflict
     (7, 6, 8, False)                 # invalid move - subgrid conflict
    ],
    ids = ["valid move", 
           "invalid move - row conflict", 
           "invalid move - column conflict",
           "invalid move - subgrid conflict"]
)
def test_isValidMove(a_valid_grid, row, col, value, expected):
    assert a_valid_grid.isValidMove(row, col, value) == expected

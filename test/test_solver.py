import sys
sys.path.append(".")
from sudoku import Solver, Grid
import pytest

@pytest.fixture()
def a_solver(a_valid_grid) -> Solver:
    return Solver(a_valid_grid)

def test_solve(a_solver, a_valid_grid):
    assert a_solver.solve() == True
    assert a_solver.grid.isValidGrid() == True
    # Check that there are no unknowns left
    assert a_solver.grid.find_empties() == []
    # solver should not modify the original grid
    for i in range(a_solver.grid.size):
        for j in range(a_solver.grid.size):
            if a_valid_grid[i, j] != 0:
                assert a_solver.grid[i, j] == a_valid_grid[i, j]


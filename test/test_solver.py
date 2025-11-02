from sudoku import Solver, Grid
import pytest
import numpy as np

@pytest.fixture()
def a_solver(a_valid_grid) -> Solver:
    return Solver(a_valid_grid)

def test_solve(a_solver, a_valid_grid):
    assert a_solver.solve() == 1  # Should find exactly one solution
    assert a_solver.grid.isValidGrid() == True
    # Check that there are no unknowns left
    assert a_solver.grid.find_empties() == []
    # solver should not modify the original grid
    for i in range(a_solver.grid.size):
        for j in range(a_solver.grid.size):
            if a_valid_grid[i, j] != 0:
                assert a_solver.grid[i, j] == a_valid_grid[i, j]

# def test_count_solutions(a_solver):
#     count = a_solver.solve(max_count=2)
#     assert count == 1  # There should be exactly one solution for a valid grid

@pytest.fixture()
def a_multiple_solutions_grid() -> Grid:
    return Grid(np.array([
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]), unknown=0)

def test_count_multiple_solutions(a_multiple_solutions_grid):
    solver = Solver(a_multiple_solutions_grid)
    count = solver.solve(max_count=3)
    assert count == 2

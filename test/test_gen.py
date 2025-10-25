from sudoku import Generator, Solver, Grid
import pytest
import numpy as np


@pytest.fixture
def template_grid() -> Grid:
    # A known valid completed Sudoku grid for testing
    completed_grid = np.array([
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ])
    return Grid(completed_grid)

@pytest.mark.parametrize("difficulty", [20, 40, 60])
def test_generate(template_grid, difficulty):
    generator = Generator(template_grid=template_grid)
    puzzle = generator.generate(difficulty=difficulty, seed=42)

    # Check 1: The returned puzzle board has the correct number of empty cells.
    assert len(puzzle.find_empties()) == difficulty

    # Check 2: The puzzle is still solvable.
    solver = Solver(puzzle)
    assert solver.solve() == True
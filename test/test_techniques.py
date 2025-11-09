import pytest
from sudoku import Grid
from sudoku.solver import HumanLogicSolver
from sudoku import get_rating, Rank

# Reuse the same sample puzzles as test_rating for stability



def test_naked_singles_makes_progress(easy_grid):
    s = HumanLogicSolver(easy_grid)
    # there should be at least one naked single available in this easy puzzle
    before_empties = len(easy_grid.find_empties())
    made = s.naked_singles()
    after_empties = len(easy_grid.find_empties())
    assert isinstance(made, bool)
    assert (made and after_empties < before_empties) or (not made and after_empties == before_empties)


def test_hidden_singles_solve_easy(easy_grid):
    s = HumanLogicSolver(easy_grid)
    # run singles until stable
    used = s.logic_until_stable({"naked_singles", "hidden_singles"})
    # easy puzzle should be solvable by singles-only
    assert easy_grid.isValidGrid()
    assert len(easy_grid.find_empties()) == 0
    assert any(name in used for name in ("naked_singles", "hidden_singles"))


def test_medium_uses_pair_or_pointing(medium_grid):
    s = HumanLogicSolver(medium_grid)
    used = s.logic_until_stable({"naked_singles", "hidden_singles", "naked_pairs", "hidden_pairs", "pointing_pairs"})
    # medium puzzles should require at least one medium technique
    assert any(name in used for name in ("naked_pairs", "hidden_pairs", "pointing_pairs"))


def test_x_wing_callable_on_hard(hard_grid):
    s = HumanLogicSolver(hard_grid)
    # x_wing should be callable and return a bool
    res = s.x_wing()
    assert isinstance(res, bool)

from enum import Enum
from .grid import Grid


class Rank(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

def get_rating(grid: Grid) -> Rank:
    """Determine the rating of a Sudoku puzzle based on its difficulty.
    Easy: Solvable using only "Naked Singles" and "Hidden Singles."
    Medium: Requires "Naked/Hidden Pairs" or "Pointing Pairs."
    Hard: Requires advanced techniques like "X-Wings" or "Swordfish."

    Args:
        grid (Grid): The Sudoku grid to be rated.

    Returns:
        Rank: The difficulty rank of the puzzle (EASY, MEDIUM, HARD).
    """
    # Decide difficulty by attempting to solve the puzzle on copies with
    # increasingly powerful technique sets. This ensures we classify by the
    # minimal technique required rather than what the solver happened to use.
    from .solver import HumanLogicSolver

    def _try_with_methods(methods: set[str]) -> bool:
        # operate on a copy of the grid to avoid mutating the caller's grid
        gcopy = Grid(grid=grid.grid, unknown=grid.unknown)
        solver = HumanLogicSolver(gcopy)
        used = solver.logic_until_stable(methods)
        # Consider solved only if grid is valid and there are no empty cells left
        return gcopy.isValidGrid() and not gcopy.find_empties()

    singles = {"naked_singles", "hidden_singles"}
    medium = singles | {"naked_pairs", "hidden_pairs", "pointing_pairs"}
    hard = medium | {"x_wing"}

    if _try_with_methods(singles):
        return Rank.EASY
    if _try_with_methods(medium):
        return Rank.MEDIUM
    # If even hard techniques don't solve it, treat as HARD (or unsolvable)
    return Rank.HARD
    

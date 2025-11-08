"""
●	Task: Implement a basic difficulty rating engine. Your engine should solve a puzzle by simulating human techniques. A simple approach is to assign a score based on the hardest technique required. For example:
○	Easy: Solvable using only "Naked Singles" and "Hidden Singles."
○	Medium: Requires "Naked/Hidden Pairs" or "Pointing Pairs."
○	Hard: Requires advanced techniques like "X-Wings" or "Swordfish."
"""

import pytest
from sudoku import get_rating, Grid, Rank

# create a easy example puzzle
@pytest.fixture
def easy_puzzle():
    # Easy: Solvable using only "Naked Singles" and "Hidden Singles."
    return Grid(grid=[
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

@pytest.fixture
def medium_puzzle():
    # Medium: Requires "Naked/Hidden Pairs" or "Pointing Pairs."
    return Grid(grid=[
        [0, 0, 5, 0, 6, 9, 0, 8, 0],
        [0, 0, 0, 5, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 0, 7],
        [0, 0, 4, 0, 8, 0, 9, 1, 0],
        [9, 0, 1, 0, 0, 3, 0, 0, 8],
        [5, 0, 0, 0, 2, 0, 0, 0, 4],
        [2, 0, 0, 9, 0, 0, 1, 0, 6],
        [7, 0, 0, 0, 0, 8, 0, 0, 0]
    ])

@pytest.fixture
def hard_puzzle():
    # Hard: Requires advanced techniques like "X-Wings" or "Swordfish."
    return Grid(grid=[
        [0, 0, 5, 3, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 7, 0, 0, 1, 0, 5, 0, 0],
        [4, 0, 0, 0, 0, 5, 3, 0, 0],
        [0, 1, 0, 0, 7, 0, 0, 0, 6],
        [0, 0, 3, 2, 0, 0, 0, 8, 0],
        [0, 6, 0, 5, 0, 0, 0, 0, 9],
        [0, 0, 4, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 9, 7, 0, 0]
    ])

def test_rating_easy(easy_puzzle):
    assert get_rating(easy_puzzle) == Rank.EASY



def test_rating_medium(medium_puzzle):
    assert get_rating(medium_puzzle) == Rank.MEDIUM

def test_rating_hard(hard_puzzle):
    assert get_rating(hard_puzzle) == Rank.HARD
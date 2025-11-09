from . import Grid
from collections import deque, defaultdict
import itertools
import random

class Solver:
    def __init__(self, grid: Grid):
        self.grid:Grid = grid
        self.empties = deque(self.grid.find_empties())
        self.history = deque(maxlen=len(self.empties))
        self.start_num = {}

    def solve(self, random_bool: bool = False, seed: int | None = None, max_count: int = 1) -> int:
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
                rotated = list(range(self.start_num.get((row, col), 1), 10)) + list(range(1, self.start_num.get((row, col), 1)))
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
        
class HumanLogicSolver():
    ALL = set(range(1, 10))
    def __init__(self, grid: Grid):
        self.grid:Grid = grid
        self.candidates: dict[tuple[int, int], set[int]] = {}
        # cache unit list for faster repeated access
        self.units = HumanLogicSolver.unit_list()
        # precompute peers for every cell to avoid recomputing sets
        self.peers: dict[tuple[int,int], set[tuple[int,int]]] = {}
        for rr in range(9):
            for cc in range(9):
                self.peers[(rr, cc)] = HumanLogicSolver.peers_of(rr, cc)
        # initial full candidate computation
        self.compute_candidates()

    @staticmethod
    def peers_of(r, c):
        row = {(r, j) for j in range(9)}
        col = {(i, c) for i in range(9)}
        br, bc = (r//3)*3, (c//3)*3
        box = {(i, j) for i in range(br, br+3) for j in range(bc, bc+3)}
        return (row | col | box) - {(r, c)}
    
    @staticmethod
    def unit_list():
        units = []
        # Rows
        for r in range(9):
            units.append({(r, c) for c in range(9)})
        # Columns
        for c in range(9):
            units.append({(r, c) for r in range(9)})
        # Boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                units.append({(r, c) for r in range(br, br+3) for c in range(bc, bc+3)})
        return units
    
    def compute_candidates(self) -> dict[tuple[int, int], set[int]]:
        # rebuild candidates from scratch for all empty cells
        self.candidates = {}
        for r in range(9):
            for c in range(9):
                if self.grid[r, c] != self.grid.unknown:
                    continue
                # start with all possibilities and remove values present in peers
                opts = set(HumanLogicSolver.ALL)
                for pr, pc in self.peers[(r, c)]:
                    val = self.grid[pr, pc]
                    if val != self.grid.unknown and val in opts:
                        opts.discard(val)
                self.candidates[(r, c)] = opts
        return self.candidates

    def set_value(self, r: int, c: int, v: int) -> bool:
        """Place value v at (r,c) and incrementally update self.candidates.

        Returns True if placement succeeded, False if invalid move.
        """
        # set on the grid (Grid will enforce internal state)
        self.grid[r, c] = v
        # remove this cell from candidates
        if (r, c) in self.candidates:
            del self.candidates[(r, c)]
        # remove v from all peers' candidate sets
        for pr, pc in self.peers[(r, c)]:
            if self.grid[pr, pc] != self.grid.unknown:
                continue
            if (pr, pc) not in self.candidates:
                continue
            opts = self.candidates[(pr, pc)]
            if v in opts:
                new_opts = set(opts)
                new_opts.discard(v)
                self.candidates[(pr, pc)] = new_opts
        return True
    
    def get_positions_in_unit(self, unit):
        # positions(dict): number -> positions in unit that can place it
        positions = defaultdict(list)
        for (r, c) in unit:
            if self.grid[r, c] == self.grid.unknown:
                for num in self.candidates.get((r, c), set()):
                    positions[num].append((r, c))
        return positions
    
    def naked_singles(self) -> bool:
        # Place the first naked single we find, then recompute candidates and return.
        for (r, c), opts in list(self.candidates.items()):
            if len(opts) == 1:
                v = next(iter(opts))
                # double-check validity (peers may have changed)
                if self.grid[r, c] == self.grid.unknown and self.set_value(r, c, v):
                    return True
        return False
    
    def hidden_singles(self) -> bool:
        # Apply the first found hidden single immediately and recompute
        # candidates so we don't create conflicting placements from different units.
        for unit in self.units:
            positions = self.get_positions_in_unit(unit)
            for num, pos_list in positions.items():
                if len(pos_list) == 1:
                    r, c = pos_list[0]
                    # double-check the move is still valid (peers may have changed)
                    if self.grid[r, c] == self.grid.unknown and self.set_value(r, c, num):
                        return True
        return False
    
    def naked_pairs(self) -> bool:
        # Find naked pairs in the Sudoku grid
        progress = False
        # For each unit (row/col/box), find two cells with identical candidate sets of size 2
        # and eliminate those two digits from other cells in the same unit.
        for unit in self.units:
            # map candidate tuple -> list of positions with that candidate set
            pair_map: dict[tuple[int, int], list[tuple[int, int]]] = {}
            for pos in unit:
                if self.grid[pos[0], pos[1]] != self.grid.unknown:
                    continue
                opts = self.candidates.get(pos)
                if opts is None:
                    continue
                if len(opts) == 2:
                    key = tuple(sorted(opts))
                    pair_map.setdefault(key, []).append(pos)

            # For any candidate-pair that appears in exactly two positions, eliminate
            # those two digits from other cells in the unit.
            for pair, positions in pair_map.items():
                if len(positions) != 2:
                    continue
                digits = set(pair)
                for pos in unit:
                    if pos in positions:
                        continue
                    if self.grid[pos[0], pos[1]] != self.grid.unknown:
                        continue
                    opts = self.candidates.get(pos)
                    if not opts:
                        continue
                    before = set(opts)
                    new_opts = opts - digits
                    if new_opts != before:
                        self.candidates[pos] = new_opts
                        progress = True
        return progress

    def hidden_pairs(self):
        progress = False
        # Hidden pairs: in a unit, find two digits that can only go in the same two cells.
        # When found, reduce those two cells' candidates to just those two digits.
        for unit in self.units:
            positions = self.get_positions_in_unit(unit)
            # consider all pairs of digits
            for a, b in itertools.combinations(range(1, 10), 2):
                pos_a = positions.get(a, [])
                pos_b = positions.get(b, [])
                if len(pos_a) == 2 and pos_a == pos_b:
                    pair_positions = pos_a
                    digits = {a, b}
                    for pos in pair_positions:
                        opts = self.candidates.get(pos, set())
                        before = set(opts)
                        new_opts = opts & digits
                        if new_opts != before:
                            self.candidates[pos] = new_opts
                            progress = True
        return progress

    def pointing_pairs(self):
        progress = False
        # Pointing pairs/triples: if in a 3x3 box all candidate positions for a digit
        # lie on the same row (or column), then that digit can be removed from the
        # rest of that row (or column) outside the box.
        # Iterate boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box = {(r, c) for r in range(br, br+3) for c in range(bc, bc+3)}
                # for each digit, check where it can be in the box
                for digit in range(1, 10):
                    positions = [pos for pos in box if self.grid[pos[0], pos[1]] == self.grid.unknown and digit in self.candidates.get(pos, set())]
                    if not positions:
                        continue
                    # all in same row?
                    rows = {p[0] for p in positions}
                    cols = {p[1] for p in positions}
                    if len(rows) == 1:
                        r = next(iter(rows))
                        for c in range(9):
                            pos = (r, c)
                            if pos in box:
                                continue
                            if self.grid[pos[0], pos[1]] != self.grid.unknown:
                                continue
                            opts = self.candidates.get(pos, set())
                            if digit in opts:
                                opts = set(opts)
                                opts.discard(digit)
                                self.candidates[pos] = opts
                                progress = True
                    # all in same column?
                    if len(cols) == 1:
                        c = next(iter(cols))
                        for r in range(9):
                            pos = (r, c)
                            if pos in box:
                                continue
                            if self.grid[pos[0], pos[1]] != self.grid.unknown:
                                continue
                            opts = self.candidates.get(pos, set())
                            if digit in opts:
                                opts = set(opts)
                                opts.discard(digit)
                                self.candidates[pos] = opts
                                progress = True
        return progress
    
    def x_wing(self):
        progress = False
        # X-Wing: for each digit, look for two rows (or columns) where the digit's
        # candidates appear in exactly the same two columns (or rows). If found,
        # eliminate that digit from other cells in those two columns (or rows).
        # Row-based X-Wing
        for digit in range(1, 10):
            # for each row, collect columns where digit can be
            row_cols = {}
            for r in range(9):
                cols = [c for c in range(9) if self.grid[r, c] == self.grid.unknown and digit in self.candidates.get((r, c), set())]
                if len(cols) == 2:
                    row_cols[r] = tuple(cols)
            # find row pairs with identical column pairs
            for r1, r2 in itertools.combinations(row_cols.keys(), 2):
                if row_cols[r1] == row_cols[r2]:
                    c1, c2 = row_cols[r1]
                    # eliminate digit from other rows in columns c1 and c2
                    for r in range(9):
                        if r in (r1, r2):
                            continue
                        for c in (c1, c2):
                            pos = (r, c)
                            if self.grid[pos[0], pos[1]] != self.grid.unknown:
                                continue
                            opts = self.candidates.get(pos, set())
                            if digit in opts:
                                new_opts = set(opts)
                                new_opts.discard(digit)
                                self.candidates[pos] = new_opts
                                progress = True

        # Column-based X-Wing (transpose)
        for digit in range(1, 10):
            col_rows = {}
            for c in range(9):
                rows = [r for r in range(9) if self.grid[r, c] == self.grid.unknown and digit in self.candidates.get((r, c), set())]
                if len(rows) == 2:
                    col_rows[c] = tuple(rows)
            for c1, c2 in itertools.combinations(col_rows.keys(), 2):
                if col_rows[c1] == col_rows[c2]:
                    r1, r2 = col_rows[c1]
                    for c in range(9):
                        if c in (c1, c2):
                            continue
                        for r in (r1, r2):
                            pos = (r, c)
                            if self.grid[pos[0], pos[1]] != self.grid.unknown:
                                continue
                            opts = self.candidates.get(pos, set())
                            if digit in opts:
                                new_opts = set(opts)
                                new_opts.discard(digit)
                                self.candidates[pos] = new_opts
                                progress = True

        return progress
    


    def logic_until_stable(self, enabled: set[str]) -> set[str]:
        used = set()
        while True:
            progress = False
            # Always try singles first inside the loop to realize previous eliminations
            for name in ("naked_singles", "hidden_singles"):
                if name in enabled and getattr(self, name)():
                    used.add(name)
                    progress = True
            # Then medium techniques
            for name in ("naked_pairs", "hidden_pairs", "pointing_pairs"):
                if name in enabled and getattr(self, name)():
                    used.add(name)
                    progress = True
            # Then hard technique(s)
            for name in ("x_wing",):
                if name in enabled and getattr(self, name)():
                    used.add(name)
                    progress = True
            if not progress:
                break
        return used    


    def solve(self) -> bool:
        """Solve the Sudoku puzzle using human-like logical techniques.
        
        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
        # Placeholder for human-like solving logic
        # Implement techniques like Naked Singles, Hidden Singles, etc.
        # Run all techniques in increasing difficulty until no further progress.
        # logic_until_stable already orders techniques (singles -> medium -> hard)
        all_methods = {"naked_singles", "hidden_singles", "naked_pairs", "hidden_pairs", "pointing_pairs", "x_wing"}
        used = self.logic_until_stable(all_methods)

        # If solver produced any progress and the grid is now valid (and filled),
        # return success and the set of techniques used. Otherwise return failed.
        solved = self.grid.isValidGrid()
        return solved, used

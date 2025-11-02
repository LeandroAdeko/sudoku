from relation_rules import groups
from assert_possibilities import if_only_one, reduce_possibilities, only_one_possibility

class SudokuMaster:

    def __init__(self, sudoku: list[list[int|list[int]]], solution: list[list[int|list[int]]] = None, debug = False):
        self.sudoku = sudoku.copy()
        self.solution = solution
        self.original_numbers: list[tuple[int,int]] = []
        self.last_modified: list[tuple[int,int]] = []
        self.count_empty()
        self.debug = debug
    
    def unit_solved(self, unit):
        return isinstance(unit, int) and unit != 0

    def count_empty(self):
        self.empty = 0
        for line, lineNumbers in enumerate(self.sudoku):
            for column, unit in enumerate(lineNumbers):
                if not self.unit_solved(unit):
                    self.empty += 1
                    continue
                self.original_numbers.append((line, column))

    def show(self, message = None, modified: list[tuple[int,int]] = []):
        """
        Prints a Sudoku board in a pretty, human-readable format.

        Args:
            board: A 9x9 list of lists representing the Sudoku board.
                Empty cells can be represented by 0 or None, or a placeholder character.
        """
        if message:
            print(f"{'*'*(60-len(message))} {message}")
        for r_idx, row in enumerate(self.sudoku):
            if r_idx % 3 == 0 and r_idx != 0:
                print("- - - - - - - - - - - - ") # Horizontal separator for 3x3 blocks

            for c_idx, num in enumerate(row):
                if c_idx % 3 == 0 and c_idx != 0:
                    print(" | ", end="") # Vertical separator for 3x3 blocks

                if c_idx == 8:
                    space = ""
                    end = "\n"
                    # print(num if num in [1,2,3,4,5,6,7,8,9] else ".", end="\n") # Print number and new line at end of row
                else:
                    space = " "
                    end = ""
                
                coordinate = (r_idx,c_idx)
                if coordinate in modified:
                    color = bcolors.OKCYAN
                else:
                    color = bcolors.BOLD if coordinate in self.original_numbers else bcolors.WARNING

                print_n = f"{color}{str(num if num in [1,2,3,4,5,6,7,8,9] else '.')}{bcolors.ENDC}"
                print(print_n + space, end=end) # Print number and space
    
    def get_block(self, lineIndex, columnIndex):
        lines = groups.get(lineIndex)
        columns = groups.get(columnIndex)

        for l in lines:
            for c in columns:
                yield self.sudoku[l][c]
    
    def get_column(self, columnIndex):
        for l in self.sudoku:
            yield l[columnIndex]

    def get_unit_relations(self, lineIndex, columnIndex):

        relations: list[int] = self.sudoku[lineIndex][:]

        relations.extend(self.get_block(lineIndex,columnIndex))
        relations.extend(self.get_column(columnIndex))

        relations = [r for r in relations if isinstance(r, int)]

        return list(set(relations))
    
    def get_number_indexes(self, block: list[int|list[int]]):
        num_idx: dict[int,list[int]] = {}
        for index, numbers in enumerate(block):
            if isinstance(numbers, int):
                continue
            for n in numbers:
                if n in block:
                    continue
                if n not in num_idx:
                    num_idx[n] = []
                num_idx[n].append(index)
        return num_idx

    def get_reversed_number_indexes(self, num_idxs: dict[int,list[int]]):
        rev_num_idx: dict[list[int], list[int]] = {}
        for number, indexes_group in num_idxs.items():
            idx_key = tuple(indexes_group)
            if idx_key not in rev_num_idx:
                rev_num_idx[idx_key] = []
            rev_num_idx[idx_key].append(number)
        return rev_num_idx


    def solve(self, solveMethods: list[str]):
        self.analyze_blocks_possibilities()
        self.solution_per_unit()
        if self.debug:
            m = f"Após analise de possibilidades e solução unitaria - {self.empty}"
            self.show(m, self.last_modified)
        self.verify_solved()

        if Methods.PER_LINE in solveMethods:
            self.solution_per_line()
            if self.debug:
                m = f"Após solução de linha - {self.empty}"
                self.show(m, self.last_modified)
        self.verify_solved()
        if Methods.PER_COLUMN in solveMethods:
            self.solution_per_column()
            if self.debug:
                m = f"Após solução de coluna - {self.empty}"
                self.show(m, self.last_modified)
        self.verify_solved()
        self.last_modified = []

    def verify_solved(self):
        if not self.solution:
            return
        for line, column in self.last_modified:
            assert self.sudoku[line][column] == self.solution[line][column]

    def solution_per_unit(self):
        self.last_modified = []
        for lineIndex, line in enumerate(self.sudoku):
            for columnIndex, unit in enumerate(line):
                if isinstance(unit, int) and unit != 0:
                    continue

                blocked_numbers = self.get_unit_relations(lineIndex, columnIndex)

                possibilities = reduce_possibilities(blocked_numbers)
                one, numbers = if_only_one(possibilities)

                self.sudoku[lineIndex][columnIndex] = numbers
                
                if one:
                    self.last_modified.append((lineIndex, columnIndex))
                    self.empty -= 1

    def solution_per_line(self):
        self.last_modified = []
        for lineIndex, line in enumerate(self.sudoku):
            unicos = only_one_possibility(line)
            for u in unicos:
                for columnIndex, unit in enumerate(line):
                    if self.unit_solved(unit):
                        continue

                    if u in unit and u not in self.get_block(lineIndex, columnIndex):
                        self.sudoku[lineIndex][columnIndex] = u
                        self.empty -= 1
                        self.last_modified.append((lineIndex, columnIndex))
    
    def solution_per_column(self):
        self.last_modified = []
        for columnIndex in range(9):
            column = self.get_column(columnIndex)
            unicos = only_one_possibility(column)
            for u in unicos:
                for lineIndex in range(len(self.sudoku)):
                    unit = self.sudoku[lineIndex][columnIndex]
                    if self.unit_solved(unit):
                        continue

                    if u in unit and u not in self.get_block(lineIndex, columnIndex):
                        self.sudoku[lineIndex][columnIndex] = u
                        self.empty -= 1
                        self.last_modified.append((lineIndex, columnIndex))

    def analyze_blocks_possibilities(self):
        def __analyze_block_possibilities(l, c):
            block = list(self.get_block(l,c))
            numbers_indexes = self.get_number_indexes(block)
            reversed_number_indexes: dict[list[int], list[int]] = self.get_reversed_number_indexes(numbers_indexes)

            for tuple_idx, numbers in reversed_number_indexes.items():
                if len(tuple_idx) == len(numbers):
                    for idx in tuple_idx:
                        block[idx] = numbers
            
            return block

        def __insert_new_block_on_sudoku(l,c,block):
            lines = groups.get(l)
            columns = groups.get(c)

            block = list(block)

            for line in lines:
                for column in columns:
                    unit = block.pop(0)

                    if isinstance(unit, int):
                        one = False
                        numbers = unit
                    else:
                        one, numbers = if_only_one(unit)

                    self.sudoku[line][column] = numbers
                    if one:
                        self.empty -= 1

        blocks_coordinates = [(2,2),(2,5),(2,8),(5,2),(5,5),(5,8),(8,2),(8,5),(8,8)]

        for l,c in blocks_coordinates:
            b = __analyze_block_possibilities(l,c)
            if b:
                # print(b)
                __insert_new_block_on_sudoku(l,c, b)

class Methods:
    PER_LINE = "LINE"
    PER_COLUMN = "COLUMN"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

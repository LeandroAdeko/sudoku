from relation_rules import groups
from assert_possibilities import if_only_one, reduce_possibilities, only_one_possibility

class SudokuMaster:

    def __init__(self, s: list[list[int|list[int]]], debug = False):
        self.sudoku = s.copy()
        self.count_empty()
        self.debug = debug
    
    def unit_solved(self, unit):
        return isinstance(unit, int) and unit != 0

    def count_empty(self):
        self.empty = 0
        for line in self.sudoku:
            for unit in line:
                if not self.unit_solved(unit):
                    self.empty += 1

    def show(self):
        """
        Prints a Sudoku board in a pretty, human-readable format.

        Args:
            board: A 9x9 list of lists representing the Sudoku board.
                Empty cells can be represented by 0 or None, or a placeholder character.
        """
        for r_idx, row in enumerate(self.sudoku):
            if r_idx % 3 == 0 and r_idx != 0:
                print("- - - - - - - - - - - - ") # Horizontal separator for 3x3 blocks

            for c_idx, num in enumerate(row):
                if c_idx % 3 == 0 and c_idx != 0:
                    print(" | ", end="") # Vertical separator for 3x3 blocks

                if c_idx == 8:
                    print(num if num in [1,2,3,4,5,6,7,8,9] else ".", end="\n") # Print number and new line at end of row
                else:
                    print(str(num if num in [1,2,3,4,5,6,7,8,9] else ".") + " ", end="") # Print number and space

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
    
    def solution_per_unit(self):
        for lineIndex, line in enumerate(self.sudoku):
            for columnIndex, unit in enumerate(line):
                if isinstance(unit, int) and unit != 0:
                    continue

                blocked_numbers = self.get_unit_relations(lineIndex, columnIndex)

                possibilities = reduce_possibilities(blocked_numbers)
                one, numbers = if_only_one(possibilities)

                self.sudoku[lineIndex][columnIndex] = numbers
                
                if one:
                    self.empty -= 1
                    if self.debug:
                        print(f"Sudoku[{lineIndex}][{columnIndex}] possibilidades: {numbers}")
                else:
                    if self.debug:
                        print(f'Sudoku[{lineIndex}][{columnIndex}] solucinado: {numbers}')

    def solution_per_line(self):
        for lineIndex, line in enumerate(self.sudoku):
            unicos = only_one_possibility(line)
            for u in unicos:
                for columnIndex, unit in enumerate(line):
                    if self.unit_solved(unit):
                        continue

                    if u in unit and u not in self.get_block(lineIndex, columnIndex):
                        self.sudoku[lineIndex][columnIndex] = u
                        self.empty -= 1





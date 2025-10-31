from sudoku_examples import sudoku_medio, sudoku_facil

from sudoku_master import SudokuMaster

master = SudokuMaster(sudoku_facil, False)

print("------------- ANTES")
master.show()

interactions = 0
max_turns = 5

while master.empty != 0 and interactions < max_turns:
    master.solution_per_unit()
    master.solution_per_line()
    interactions += 1
    print(f"Interação {interactions} finished with {master.empty}")

print("-------------------")
master.show()
print("DEPOIS ------------")

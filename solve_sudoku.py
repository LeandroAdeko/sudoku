from sudoku_examples import sudoku_medio, sudoku_facil, sudoku_facil_solucao

from sudoku_master import SudokuMaster, Methods

master = SudokuMaster(sudoku_facil, sudoku_facil_solucao, True)

print(f"------------- COMEÇO - {master.empty}")
master.show()

interactions = 0
max_turns = 7

while master.empty != 0 and interactions < max_turns:
    master.solve([
        Methods.PER_COLUMN,
        Methods.PER_LINE,
    ])
    interactions += 1

print("-------------------")
master.show()
print("DEPOIS ------------")

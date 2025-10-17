
def print_sudoku(board):
    """
    Prints a Sudoku board in a pretty, human-readable format.

    Args:
        board: A 9x9 list of lists representing the Sudoku board.
               Empty cells can be represented by 0 or None, or a placeholder character.
    """
    for r_idx, row in enumerate(board):
        if r_idx % 3 == 0 and r_idx != 0:
            print("- - - - - - - - - - - - ") # Horizontal separator for 3x3 blocks

        for c_idx, num in enumerate(row):
            if c_idx % 3 == 0 and c_idx != 0:
                print(" | ", end="") # Vertical separator for 3x3 blocks

            if c_idx == 8:
                print(num if num in [1,2,3,4,5,6,7,8,9] else ".", end="\n") # Print number and new line at end of row
            else:
                print(str(num if num in [1,2,3,4,5,6,7,8,9] else ".") + " ", end="") # Print number and space

sudoku_medio: list[list[int]] = [
    [ 4,5,0,9,0,0,0,0,0 ],
    [ 9,0,3,0,0,0,0,2,0 ],
    [ 0,0,0,3,0,0,6,5,0 ],
    [ 8,0,0,0,0,7,0,0,2 ],
    [ 1,0,0,0,0,6,9,0,0 ],
    [ 0,0,0,0,0,0,0,0,0 ],
    [ 0,0,0,0,0,2,0,0,1 ],
    [ 0,0,8,1,0,0,0,7,0 ],
    [ 0,0,5,0,9,0,0,0,4 ]
]


example_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]



lines_123 = [0,1,2]
lines_456 = [3,4,5]
lines_789 = [6,7,8]

columns_147 = [0,3,6]
columns_258 = [1,4,7]
columns_369 = [2,5,8]

groups = {
    0: lines_123,
    1: lines_123,
    2: lines_123,
    3: lines_456,
    4: lines_456,
    5: lines_456,
    6: lines_789,
    7: lines_789,
    8: lines_789,
}

def get_block(_sudoku: list[list[int]], lineIndex, columnIndex):
    lines = groups.get(lineIndex)
    columns = groups.get(columnIndex)

    for l in lines:
        for c in columns:
            yield _sudoku[l][c]

def get_column(_sudoku: list[list[int]], columnIndex):
    for l in _sudoku:
        yield l[columnIndex]


from sudoku_examples import print_sudoku, sudoku_medio

from relation_rules import get_block, get_column

from assert_possibilities import reduce_possibilities, if_only_one, desired

def get_relations(_sudoku: list[list], lineIndex: int, columnIndex: int):

    relations: list[int] = _sudoku[lineIndex][:]

    relations.extend(get_block(_sudoku,lineIndex,columnIndex))
    relations.extend(get_column(_sudoku,columnIndex))

    relations = [r for r in relations if isinstance(r, int)]

    return list(set(relations))
    
sudoku = sudoku_medio.copy()

for lineIndex, line in enumerate(sudoku):
    for columnIndex, unit in enumerate(line):
        if unit:
            continue

        blocked_numbers = get_relations(sudoku, lineIndex, columnIndex)

        possibilities = reduce_possibilities(blocked_numbers)
        one, numbers = if_only_one(possibilities)

        sudoku[lineIndex][columnIndex] = numbers
        
        if one:
            print(f'Sudoku[{lineIndex}][{columnIndex}] solucinado: {numbers}')
        else:
            print(f"Sudoku[{lineIndex}][{columnIndex}] possibilidades: {numbers}")

print_sudoku(sudoku)

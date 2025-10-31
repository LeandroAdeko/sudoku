from collections import Counter

desired = [1,2,3,4,5,6,7,8,9]

def if_only_one(numbers: list[int]):
    if len(numbers) == 1:
        return True, numbers[0]
    else:
        return False, numbers

def only_one_possibility(numbers: list[int]):

    todos_numeros = [num for sublista in numbers if isinstance(sublista, list) for num in sublista]

    contagem = Counter(todos_numeros)

    unicos = {num for num, qtd in contagem.items() if qtd == 1}

    return unicos

def reduce_possibilities(reduce: list[int], possibilities: list[int] = desired):
    return list(set(possibilities) - set(reduce))

def intersect(list1, list2):
    return list(set(list1) & set(list2))



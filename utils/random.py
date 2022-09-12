from random import choice

def choices(li: list, amt: int = 1):
    values = []

    if len(li) < amt:
        raise Exception('Not enough elements to return a list.')
    
    copy_list = list(li)

    for i in range(amt):
        rand = choice(copy_list)
        values.append(rand)
        copy_list.remove(rand)
    
    return values
    
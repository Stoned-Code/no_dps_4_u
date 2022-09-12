from random import choice

def choices(li: list, amt: int = 1) -> list:
    """
    Picks random choices with the amount given from the list given.

    Arguments:
    ----------
    li: `list`
        List of items to select from.
    amt: `int`
        The amount of items you went selected from the list.
    """
    # Creates an empty list.
    values = [] 

    # If the length of the list is lower then the amount expected, an error is thrown.
    if len(li) < amt:
        raise Exception('Not enough elements to return a list.')
    # Creates a copy of the given list.
    copy_list = list(li) 


    for i in range(amt):
        rand = choice(copy_list) # Chooses a item object from the copy of the list.
        values.append(rand) # Adds the item to the values list. 
        copy_list.remove(rand) # Removes the given item from the copy.
    
    return values # Returns the chosen values.
    
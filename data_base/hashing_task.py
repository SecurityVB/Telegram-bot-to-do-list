class DbSymbols:
    db_task_done = '-~*t1*~-'
    db_task_not_done = '-~*t0*~-'
    task_space = '-~*ts*~-'


def find_keys_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return False


def create_hash_dict(symbols):
    hash_dict = {}
    for i in range(len(symbols) - 1):
        symbol = symbols[i]
        hash_dict[symbol] = f"A9-~{symbol}~-A9"
    return hash_dict


def hashing_(stroka, dictionary):
    result = stroka
    for i in dictionary.keys():
        if i in stroka:
            result = result.replace(i, hasher[i])
    return result



def rehashing_(hash_stroka, dictionary):
    result = hash_stroka
    for i in dictionary.values():
        if i in result:
            key = find_keys_by_value(dictionary, i)
            result = result.replace(i, key)
    return result


symbols = "</>`~?*&^:%$#@|}{="
hasher = create_hash_dict(symbols)
def sum_dict(dict_one, dict_two):
    for value in dict_one:
        dict_one[value] = float(dict_one[value])
    for item in dict_two:
        dict_one[item] = float(dict_two[item])
    return dict_one

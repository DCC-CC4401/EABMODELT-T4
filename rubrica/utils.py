# auxiliary functions

def rubric_to_table(rubric):
    """

    :param rubric: dict
    :return: [][]
    """
    table = []  # table[rows][columns]

    # header
    decimals = [float(key) for key in rubric[0] if key != "aspecto"]
    decimals.sort()
    table.append([""] + [str(value) for value in decimals])

    # body
    for row in rubric:  # row is a dict
        table.append(
            [row.pop("aspecto")] + [value for key, value in sorted(row.items(), key=lambda item: float(item[0]))])

    return table

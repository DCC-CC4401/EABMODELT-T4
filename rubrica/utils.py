# auxiliary functions

def rubric_to_table(rubric):
    """

    :param rubric: [] of dicts
    :return: [][]
    """
    table = []  # table[rows][columns]

    # header
    table.append([key for key, value in rubric[0].items()])

    # body
    for row in rubric:  # row is a dict
        table.append([value for key, value in row.items()])

    return table


def pair_search(position, seq, ss):
    """
    :param position: the index of target position
    :param seq: the sequence of RNA containing A, U, G, C
    :param ss: the secondary structure of the RNA
    :return: the index of the paired position
    """

    if position < 0 or position > len(seq):
        raise ValueError("position out of range")
    if len(seq) != len(ss):
        raise ValueError("sequence and secondary structure do not match")

    if ss[position] != '(' and ss[position] != ')':
        return

    temp_count = 0
    temp_position = position
    direction = 0
    if ss[position] == '(':
        temp_count += 1
        temp_position += 1
        direction = 1
    elif ss[position] == ')':
        temp_count -= 1
        temp_position -= 1
        direction = -1
    while temp_count != 0:
        if direction == 1:
            if ss[temp_position] == '(':
                temp_count += 1
                temp_position += 1
            elif ss[temp_position] == ')':
                temp_count -= 1
                temp_position += 1
            else:
                temp_position += 1
        elif direction == -1:
            if ss[temp_position] == '(':
                temp_count += 1
                temp_position -= 1
            elif ss[temp_position] == ')':
                temp_count -= 1
                temp_position -= 1
            else:
                temp_position -= 1
    if direction == 1:
        temp_position -= 1
    elif direction == -1:
        temp_position += 1
    return seq[temp_position], ss[temp_position]

print(pair_search(0,"1234GGAAAA5678","((((.()...))))"))
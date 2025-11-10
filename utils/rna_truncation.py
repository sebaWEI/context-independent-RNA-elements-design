from pair_search import pair_search


def marginal_rna_truncation(seq, ss, any_unpaired_position):
    """

    :param seq: the RNA sequence
    :param ss: the RNA secondary structure
    :param any_unpaired_position: the index of any unpaired position, the truncation will occur round this loop
    :return: the marginally truncated RNA sequence
    """
    temp = 0
    position = None
    if ss[any_unpaired_position] != "(" and ss[any_unpaired_position] != ")":
        for i in range(any_unpaired_position, len(ss)):
            if ss[i] == ")":
                temp = 1
            elif ss[i] != ")" and temp == 1:
                position = i - 1
                break
        pair_position = pair_search(seq, ss, position)[0]
        seq = seq[:position] + seq[position + 1:]
        seq = seq[:pair_position] + seq[pair_position + 1:]
        return seq
    else:
        raise Exception('any_unpaired_position must be a index of a unpaired nucleotide')

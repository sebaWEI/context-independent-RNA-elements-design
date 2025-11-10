from pair_search import pair_search
import random


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


def random_rna_truncation(seq, ss, any_unpaired_position, truncation_length):
    """
    :param seq: the RNA sequence
    :param ss: the RNA secondary structure
    :param any_unpaired_position: the index of any unpaired position, the truncation will occur round this loop
    :return: the marginally truncated RNA sequence
    """
    temp = 0
    start = 0
    end = 0
    if ss[any_unpaired_position] != "(" and ss[any_unpaired_position] != ")":
        for i in range(any_unpaired_position, len(ss)):
            if ss[i] == ")":
                if temp == 0:
                    temp = 1
                    start = i
            elif ss[i] != ")" and temp == 1:
                end = i - 1
                break
        positions = random.sample(range(start, end + 1), truncation_length)
        paired_positions = []
        for i in positions:
            paired_positions.append(pair_search(seq, ss, i)[0])
            print(paired_positions)
        total_positions = positions + paired_positions
        print(total_positions)
        new_seq = ''.join([c for i, c in enumerate(seq) if i not in total_positions])
        return new_seq
    else:
        raise Exception('any_unpaired_position must be a index of a unpaired nucleotide')

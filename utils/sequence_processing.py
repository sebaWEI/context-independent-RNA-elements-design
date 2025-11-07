def rna_processing(seq):
    if not isinstance(seq, str):
        raise Exception('seq must be a string')
    seq = seq.upper()
    for i in seq:
        if i not in ['A', 'U', 'G', 'C', 'T']:
            raise Exception('seq must start with A or U or G or C (or T)')

    seq = ''.join('U' if b == 'T' else b for b in seq)

    return seq



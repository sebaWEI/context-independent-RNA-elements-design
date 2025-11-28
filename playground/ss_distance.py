def find_motif_from_right(seq, motif="UAUUGAGU"):
    position = seq.rfind(motif)

    if position == -1:
        return None

    return position


from pathlib import Path
from shortest_path import get_shortest_path

ss_path = Path(__file__).parent / "predicted_ss.txt"
with open(ss_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        if i < len(lines) and lines[i].strip().startswith('>'):
            name = lines[i].strip()[1:]
            if i + 1 < len(lines):
                seq = lines[i + 1].strip()
            else:
                seq = ""
            start_position = find_motif_from_right(seq, "UAUUGAGU")
            j = i + 2
            length_set = set()
            while j < len(lines) and not (lines[j].strip().startswith('>')):
                ss = lines[j].strip()
                j += 1

                if start_position is not None:
                    length = get_shortest_path(ss, start_position)
                    if length not in length_set:
                        length_set.add(length)
                        print(name, length, start_position)

                else:
                    print(f"{name}: UAUUGAGU motif not found")
                    break

            i += 1
        else:
            i += 1

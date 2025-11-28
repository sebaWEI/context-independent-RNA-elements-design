import sys
import os
import csv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from utils.viennarna import ss_predict, sub_predict


def predict_structure(csv_path, output_path, mode='full', verbose=True):
    if mode not in ['full', 'insert']:
        raise ValueError("mode must be 'full' or 'insert'")

    existing_indices = set()
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        with open(output_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('>'):
                    idx = line[1:].strip()
                    existing_indices.add(idx)
                    i += 1
                else:
                    i += 1

    skipped_count = 0
    processed_count = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            reader.fieldnames = [name.strip() for name in reader.fieldnames]

        with open(output_path, "a", encoding="utf-8") as out_f:
            for row in reader:
                idx = row['idx']

                if idx in existing_indices:
                    skipped_count += 1
                    if verbose:
                        print(f"skip {idx} (existing in file)")
                    continue

                seq = row['seq']

                if mode == 'full':
                    seq_fragment = seq
                    position_info = "full sequence"
                elif mode == 'insert':
                    start_nuc = int(row['start_nuc'])
                    end_nuc = int(row['end_nuc'])
                    seq_fragment = seq[start_nuc:end_nuc + 1]
                    position_info = f"position {start_nuc}-{end_nuc}"
                    print(seq_fragment)

                if seq_fragment == "":
                    print(f"{idx}: empty fragment")
                else:
                    ss, mfe = ss_predict(seq_fragment)
                    # sub_structures = sub_predict(seq_fragment)

                    out_f.write(f">{idx}\n")
                    out_f.write(f"{seq_fragment}\n")
                    out_f.write(f"{ss}\n")
                    # for sub_structure in sub_structures:
                    #     out_f.write(f"{sub_structure}\n")

                    existing_indices.add(idx)
                    processed_count += 1

                    if verbose:
                        print(f"sequence: {idx}")
                        print(f"fragment: ({position_info}): {seq_fragment}")
                        print(f"secondary structure: {ss}")
                        print(f"MFE: {mfe:.2f} kcal/mol")
                        print("-" * 80)

    if verbose:
        print(f"\nprocessing done: added {processed_count} sequences，skipped {skipped_count} sequences")
        print(f"results saved to: {output_path}")


if __name__ == "__main__":
    csv_path = os.path.join(current_dir, "data.csv")
    output_path = os.path.join(current_dir, "predicted_ss.txt")
    predict_structure(csv_path, output_path, mode='full', verbose=True)

import csv
import pickle

HHBLITS_AA_TO_ID = {'A': 0, 'B': 2, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'J': 20, 'K': 8, 'L': 9, 'M': 10, 'N': 11, 'O': 20, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'U': 1, 'V': 17, 'W': 18, 'X': 20, 'Y': 19, 'Z': 3, '-': 21}
restypes_with_x_and_gap = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'X', '-']
restypes_with_x = ['?'] * 22
for k,v in HHBLITS_AA_TO_ID.items():
    if k in restypes_with_x_and_gap:
        restypes_with_x[v] = k

def get_af2_msa(seq):
    import hashlib, os, gzip
    md5 = hashlib.md5(seq.encode('utf-8')).hexdigest()
    feature_file = f'./Database/MSA_Features/{md5}.pkl.gz'
    if not os.path.exists(feature_file):
        return None
    else:
        ft = pickle.load(gzip.open(feature_file, 'rb'))
        msa = [ "".join([ restypes_with_x[id_] for id_ in seq ]) for seq in ft['msa'] ]
    return msa

case2query = {}
with open('./experiment/selected_benchmark_dataset.tsv', 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        case2query[row['Name']] = row['Seq']

case2msa = {}
for case, seq in case2query.items():
    print(case)
    msa = get_af2_msa(seq)
    # breakpoint()
    case2msa[case] = msa
breakpoint()
pickle.dump(case2msa, open('./bm160case2msa.pkl', 'wb'))
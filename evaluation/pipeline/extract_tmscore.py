import os
import pickle
import csv

my_dir = 'dynamic-id-res'

# for all the files formatted as "AF2_*.txt" in the current directory, add them to file-list
file_list = []
for file in os.listdir(f'./{my_dir}'):
    if file.startswith('AF2_') and file.endswith('_TMscore.txt'):
        file_list.append(file)

tm_scores = {}

idx2bs = {}
with open('./experiment/selected_benchmark_dataset.tsv', 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        name = row['Name']
        single = row['AF2_Single']
        uni = row['Af2_UniClust30']
        uni_top = row['Af2_UniClust30_Top64']
        full = row['AF2_MSA']
        idx2bs[name] = {'single': float(single), 'uni': float(uni), 'uni_top': float(uni_top), 'full': float(full)}

subset = pickle.load(open('./experiment/benchmark40_name2id.pkl', 'rb'))
ref = pickle.load(open('./experiment/benchmark/aextracted_tm_scores.pkl', 'rb'))
for file in file_list:
    print(file)
    substr = file.split('AF2_')[1].split('_TMscore.txt')[0]
    print(substr)
    if substr not in subset.keys():
        continue
    tm_scores[substr] = idx2bs[substr]

    with open(f'./{my_dir}/{file}', 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'TM-score' in line:
            parts = line.split()
            tm_score = float(parts[-3])
            if 'BASELINE' in line:
                prefix = parts[1]
                tm_scores[substr][f'{prefix}-baseline'] = tm_score
            else:
                exp = '-'.join(parts[1:5])
                tm_scores[substr][exp] = tm_score
    
    for prefix in [1, 3, 6]:
        if f'{prefix}-baseline' not in tm_scores[substr].keys():
            tm_scores[substr][f'{prefix}-baseline'] = ref[substr][f'{prefix}-baseline']

print(len(tm_scores.keys()))
with open(f'./{my_dir}/extracted_tm_scores.pkl', 'wb') as file:
    pickle.dump(tm_scores, file)

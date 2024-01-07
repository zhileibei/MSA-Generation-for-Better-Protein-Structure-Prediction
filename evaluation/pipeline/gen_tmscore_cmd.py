import re
import os
import csv
import pickle

subset = pickle.load(open('./experiment/benchmark40_name2id.pkl', 'rb'))


idx2gt = {}
with open('./experiment/selected_benchmark_dataset.tsv', 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        name = row['Name']
        if name not in subset.keys():
            continue
        idx2gt[name] = f"./MSA_Generation/data/Benchmark/GT/{name}.pdb"

prefix = [0, 1, 3, 6]
my_dir = 'dynamic-id/'

exp2batchfile = {}
for p in prefix:
    cnt = 0
    for bfn in idx2gt.keys():
        file_dir = f'./experiment/{my_dir}msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_{p}_gpt'
        bf = f'{file_dir}/batch-{bfn}.lst'
        if not os.path.exists(bf):
            cnt += 1
            continue
        
        with open(bf, 'r') as file:
            lines = file.readlines()
        
        for i in range(len(lines)):
            line = lines[i].strip()

            # example: 'tmp_1.0_p_0.0_k_5_prefix_0_res_idx_0_num_11_descend_True_nocontext.txt'

            assert bfn in line
            idx_value = bfn
            if idx_value not in exp2batchfile:
                exp2batchfile[idx_value] = {} # 38 cases
            
            assert f'prefix_{p}' in line
            prefix_value = p
            if prefix_value not in exp2batchfile[idx_value]:
                exp2batchfile[idx_value][prefix_value] = {} # 0, 1, 3, 6

            if line.endswith('baseline.txt'):
                exp2batchfile[idx_value][prefix_value]['baseline'] = f'{file_dir}/{bfn}_{i}.pdb'
                continue

            p_k_value = re.search(r'p_[0-9]*\.[0-9]_k_[0-9]*', line).group()
            if p_k_value not in exp2batchfile[idx_value][prefix_value]:
                exp2batchfile[idx_value][prefix_value][p_k_value] = {}
    
            num_value = int(re.search(r'num_([0-9]*)', line).group(1))
            if num_value not in exp2batchfile[idx_value][prefix_value][p_k_value]:
                exp2batchfile[idx_value][prefix_value][p_k_value][num_value] = {}

            # descend_value = re.search(r'descend_(True|False)', line).group(1)
            nocontext_value = re.search(r'_nocontext', line)
            if nocontext_value:
                exp2batchfile[idx_value][prefix_value][p_k_value][num_value]['w/o_context'] = f'{file_dir}/{bfn}_{i}.pdb'
            else:
                exp2batchfile[idx_value][prefix_value][p_k_value][num_value]['w/_context'] = f'{file_dir}/{bfn}_{i}.pdb'
    print(cnt)


# breakpoint()
import pickle
pickle.dump(exp2batchfile, open(f'./experiment/{my_dir}exp2batchfile.pkl', 'wb'))
            
for idx, gt_file in idx2gt.items():
    with open(f'./experiment/{my_dir[:-1]}-res/calc_TMscore_{idx}.sh', 'a') as output_file:
        output_file.write(f"output_file=\"AF2_{idx}_TMscore.txt\"\n")     
        output_file.write("\n")     
        output_file.write("\n")
        for prefix, p in sorted(exp2batchfile[idx].items()): # few_shot prefix (0, 1, 3, 6)
            if int(prefix) > 0:
                output_file.write(f"current_output=$(TMscore {exp2batchfile[idx][prefix]['baseline']} {gt_file} -seq | grep \"TM-score    = \")\n")
                output_file.write(f"echo \"{idx} {prefix} BASELINE $current_output\" >> \"$output_file\"\n")
                output_file.write("\n")
            for strategy, st in sorted(p.items()): # strategy
                if strategy == 'baseline':
                    continue
                for num, n in sorted(st.items()): # gen num
                    for context, c in sorted(n.items()): # w/o or w/ context
                        output_file.write(f"current_output=$(TMscore {exp2batchfile[idx][prefix][strategy][num][context]} {gt_file} -seq | grep \"TM-score    = \")\n")
                        output_file.write(f"echo \"{idx} {prefix} {strategy} {num} {context} RES $current_output\" >> \"$output_file\"\n")
                        output_file.write("\n")


    
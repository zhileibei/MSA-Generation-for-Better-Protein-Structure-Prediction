import matplotlib.pyplot as plt
import numpy as np

# calculate MSA generation time
with open('generate_0shot.log', 'r') as file:
    lines = file.readlines()
    seq_len = []
    gen_time = []
    for line in lines:
        if 'Input:' in line:
            seqlen = len(line.split('[\'')[1].split('\']')[0])
            seq_len.append(seqlen)
        elif 'Taken time' in line:
            gentime = float(line.split('Taken time ')[1].split(' path')[0])
            gen_time.append(gentime)
# calculate time per token
time_per_token = [gen_time[i]/seq_len[i] for i in range(len(seq_len))]
average_time_per_token = np.mean(time_per_token) / 49
print(average_time_per_token)

# calculate prediction time with generated MSA
with open('pred_generated.log', 'r') as file:
    lines = file.readlines()
    pred_time_gen = []
    for line in lines:
        if 'round time used ' in line:
            predtime = float(line.split('round time used ')[1].split(' sec')[0])
            pred_time_gen.append(predtime)

# calculate prediction time with MSA search
with open('pred_search.log', 'r') as file:
    lines = file.readlines()
    seq_len_10 = []
    msa_search_time = []
    pred_time_search = []
    for line in lines:
        if 'Start to run AF2 MSA process' in line:
            seqlen = len(line.split('Start to run AF2 MSA process: ')[1].split('\n')[0])
            seq_len_10.append(seqlen)
        if 'MSA search time: ' in line:
            searchtime = float(line.split('MSA search time: ')[1].split('\n')[0])
            msa_search_time.append(searchtime)
        if 'round time used ' in line:
            predtime = float(line.split('round time used ')[1].split(' sec')[0]) - searchtime
            pred_time_search.append(predtime)

gen_time = [average_time_per_token * seq_len[i] * 8 for i in range(len(seq_len_10))]
total_time_gen = [gen_time[i] + pred_time_gen[i] for i in range(len(seq_len_10))]
total_time_search = [pred_time_search[i] + msa_search_time[i] for i in range(len(seq_len_10))]

print(np.mean(gen_time)) # MSA generation time
print((np.mean(pred_time_gen) + np.mean(pred_time_search))/2) # prediction time
print(np.mean(total_time_gen)) # total time for MSA-generation pipeline
print(np.mean(msa_search_time)) # MSA search time
print((np.mean(pred_time_gen) + np.mean(pred_time_search))/2) # prediction time
print(np.mean(total_time_search)) # total time for MSA-search pipeline


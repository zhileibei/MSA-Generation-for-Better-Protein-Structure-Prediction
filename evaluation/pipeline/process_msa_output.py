from collections import defaultdict
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def calculate_sequence_identity(seq1, seq2):
    matches = sum(res1 == res2 for res1, res2 in zip(seq1, seq2))
    try:
        identity = matches / min(len(seq1), len(seq2))
    except:
        # print(seq1, seq2)
        pass
    return identity

total_seq_ids = []

def process(inputs, gen, prefix):
    def cal_ids(msas, pri_seq):
        ranks = []
        for _ in msas:
            try:
                assert len(_) == len(pri_seq)
            except:
                # print(len(_), len(pri_seq))
                # print(idx, f"{gen}/{name}")
                continue
                # assert len(_) == (len(pri_seq) - 1)
                # _ = _ + '-'
            seq_id = calculate_sequence_identity(pri_seq, _)
            ranks.append((_, seq_id))
        # sorted_rank = sorted(ranks, key = itemgetter(1), reverse = True)
        # return sorted_rank
        return ranks


    idx2input = {}
    with open(inputs, 'r') as f:
        ps = f.read().splitlines()
        for line in ps:
            # idx, data = line.split('_')
            idx, data = line.split(':')
            # print(idx)
            idx2input[idx] = data
    idx2prefix = {}
    for idx, seqs in idx2input.items():
        msas = seqs.split('<M>')
        pri_msa = msas[0]
        # pre_msa = '<M>'.join(msas[1:(prefix + 1)])
        # tmp = {'query': pri_msa, 'context': pre_msa}
        tmp = {'query': pri_msa}
        idx2prefix[idx] = tmp
    for name in os.listdir(gen):
        # output = defaultdict(set)
        output = {}
        with open(os.path.join(gen, name), 'r') as f:
            res = f.read().splitlines()
        for line in res:
            # idx, data = line.split('_')
            idx, data = line.split(':')
            msas = data.split('[<M>]')
            pre_msa = '<M>'.join(msas[1:(prefix + 1)])
            gen_msa = msas[(prefix + 1):]
            # q_pre_msa = idx2prefix[idx]['context']
            # assert q_pre_msa == pre_msa
            idx2prefix[idx]['context'] = pre_msa
            for _ in gen_msa:
                # if len(_) != 0:
                # output[idx].add(_)
                if idx not in output:
                    output[idx] = []
                output[idx].append(_)

        path = f'{output_dirs}/{gen}'
        os.makedirs(path, exist_ok=True)
        # output_res = open(f'{output_dirs}/{gen}/{name}_res', 'w')
        # print()
        save_res = {}
        for idx, msas in output.items():
            pri_seq = idx2prefix[idx]['query']
            pre_msa = idx2prefix[idx]['context'].split('<M>')
            gen_msa = msas
            if prefix > 0:
                pre_res = cal_ids(pre_msa, pri_seq)
            else:
                pre_res = None
            gen_res = cal_ids(gen_msa, pri_seq)
            tmp = {
                'query': pri_seq,
                'context': pre_res,
                'generate': gen_res
            }
            save_res[idx] = tmp
        import json
        with open(f'{output_dirs}/{gen}/{name}_res.json', 'w') as f:
            json.dump(save_res, f, indent = 4)
        
        import pickle
        with open(f'{output_dirs}/{gen}/{name}_res.pkl', 'wb') as f:
            pickle.dump(save_res, f)

import os
output_dirs = "msa_generation_result"
process("msa_benchmark_input", "msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_0_gpt", prefix = 0)
process("msa_benchmark_input", "msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_1_gpt", prefix = 1)
process("msa_benchmark_input", "msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_3_gpt", prefix = 3)
process("msa_benchmark_input", "msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_6_gpt", prefix = 6)
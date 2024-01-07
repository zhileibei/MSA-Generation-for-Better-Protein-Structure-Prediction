import pickle
import os

output_basedir = './experiment/dynamic-id'

subset = pickle.load(open('./experiment/benchmark40_name2id.pkl', 'rb'))

def calculate_sequence_identity(seq1, seq2):
    matches = sum(res1 == res2 for res1, res2 in zip(seq1, seq2))
    try:
        identity = matches / min(len(seq1), len(seq2))
    except:
        print(seq1, seq2)
    return identity

def calc_average_similarity(new_sequence, existing_sequences):
    """Calculate the average similarity of a new sequence with a list of existing sequences."""
    if not existing_sequences:
        return 0
    total_similarity = sum(calculate_sequence_identity(new_sequence, seq[0]) for seq in existing_sequences)
    return total_similarity / len(existing_sequences)

def custom_sort(query, sequences):
    """Sort the sequences based on the average similarity with all prior sequences."""
    sorted_sequences = [(query, 1.0)]
    while sequences:
        # Find the sequence with the highest average similarity to the sequences already sorted
        next_sequence = min(sequences, key=lambda seq: calc_average_similarity(seq, sorted_sequences))
        sorted_sequences.append((next_sequence, calc_average_similarity(next_sequence, sorted_sequences)))
        sequences.remove(next_sequence)
    return sorted_sequences[1:]


def process_gen(input_fn, num, descend=True):
    input_dir = input_fn.split('/')[-2]
    input_file = input_fn.split('/')[-1]
    data = pickle.load(open(input_fn, 'rb'))
    for idx, case in data.items():
        if idx not in subset.keys():
            continue
        query = case['query']
        context = case['context']
        generate = case['generate']

        # sort generate
        generate.sort(key=lambda x: x[1], reverse=descend)
        generate_ori = [g[0] for g in generate]
        generate = custom_sort(query, generate_ori)
        if [g[0] for g in generate] == generate_ori:
            print('identical')

        output_dir = os.path.join(output_basedir, input_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        fn = input_file.replace('.pkl', '')
        
        if context is not None:
            output_fn = os.path.join(output_dir, f'{fn}_idx_{idx}_num_{num}_descend_{descend}.txt')
            with open(output_fn, 'w') as f:
                f.write(f'{query}\n')
                for c in context:
                    f.write(f'{c[0]}\t{c[1]}\n')
                for g in generate[:num]:
                    f.write(f'{g[0]}\t{g[1]}\n')
        
        output_fn = os.path.join(output_dir, f'{fn}_idx_{idx}_num_{num}_descend_{descend}_nocontext.txt')
        with open(output_fn, 'w') as f:
            f.write(f'{query}\n')
            for g in generate[:num]:
                f.write(f'{g[0]}\t{g[1]}\n')

descend_order = True
for num in [1, 4, 8, 12, 16, 24, 32, 48]:
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_0_gpt/tmp_1.0_p_0.0_k_5_prefix_0_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_0_gpt/tmp_1.0_p_1.0_k_0_prefix_0_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_1_gpt/tmp_1.0_p_0.0_k_5_prefix_1_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_1_gpt/tmp_1.0_p_1.0_k_0_prefix_1_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_3_gpt/tmp_1.0_p_0.0_k_5_prefix_3_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_3_gpt/tmp_1.0_p_1.0_k_0_prefix_3_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_6_gpt/tmp_1.0_p_0.0_k_5_prefix_6_res.pkl", num, descend_order)
    process_gen("./msa_generation_result/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_6_gpt/tmp_1.0_p_1.0_k_0_prefix_6_res.pkl", num, descend_order)

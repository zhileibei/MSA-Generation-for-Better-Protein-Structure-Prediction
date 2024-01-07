import os

prefix = ['0', '1', '3', '6']
for p in prefix:
    my_dir = f'./experiment/dynamic-id/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_{p}_gpt'
    # put all the filenames (without directory) of files under dir into a .lst file
    for root, dirs, files in os.walk(my_dir):
        # breakpoint()
        files.sort()
        for file in files:
            if file.endswith('.fasta') or file.endswith('.txt'):
                idx = '_'.join(file.split('idx_')[1].split('_')[:2])
                with open(f'{my_dir}/batch-{idx}.lst', 'a') as f:
                    f.write(f'{file}\n')
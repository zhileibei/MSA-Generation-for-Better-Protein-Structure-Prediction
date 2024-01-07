import re
import os


prefix = [0, 1, 3, 6]
gpus = [0, 1, 2, 3]

for idx, p in enumerate(prefix):
    my_dir = f'./experiment/dynamic-id/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_{p}_gpt'
    # put all the filenames (without directory) of files under dir into a .lst file
    for root, dirs, files in os.walk(my_dir):
        batches = []
        for file in files:
            if file.endswith(".lst"):
                batches.append(file)
        batches.sort()
        print(len(batches))
        for i in range(8):
            with open(os.path.join(my_dir, f"script_{i}.sh"), "w") as f:
                f.write('source init_af2_env.sh\n')
                f.write(f'cd {my_dir}\n')
                for j in range(int(i*(len(batches) / 8)), min(len(batches), int((i+1)*(len(batches) / 8)))):
                    f.write(f"CUDA_VISIBLE_DEVICES={gpus[idx]} run_af2.py {batches[j]} {batches[j].split('-')[1].split('.')[0]}\n")
        
        
import subprocess
import sys
import os
import concurrent.futures

if len(sys.argv) < 2:
    print("Usage: python run_all.py <prefix_num>")
    sys.exit(1)

p = sys.argv[1]
print(p)
my_dir = f"dynamic-div/msa_benchmark_input_msa_gen_150m_10240_tied_hq_data_sat_129000_{p}_gpt"

if not os.path.isdir(my_dir):
    print("Please provide a valid directory path.")
    sys.exit(1)

# Define the paths to your bash scripts
script_paths = [f'{my_dir}/script_{i}.sh' for i in range(8)]

# Function to run a bash script
def run_script(script_path):
    subprocess.run(['bash', script_path])

# Function to execute a script using subprocess.run
def execute_script(script):
    subprocess.run(['bash', script])

# Execute the scripts using concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(execute_script, script_paths)

print("All scripts have finished executing.")

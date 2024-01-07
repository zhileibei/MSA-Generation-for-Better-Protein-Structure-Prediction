#!/bin/bash
#SBATCH --job-name=inference
#SBATCH --partition=long                           # Ask for unkillable job
#SBATCH --cpus-per-task=4                              # Ask for 2 CPUs
#SBATCH --nodes=1
#SBATCH --gres=gpu:a100l:1
#SBATCH --ntasks-per-node=1                               # Ask for 1 GPU
#SBATCH --mem=128G                                        # Ask for 10 GB of RAM
#SBATCH --time=20:00:00                                   

# module load miniconda/3
# conda init
# conda activate openflamingo

# cd ~/scratch/github_clone/MSA-Augmentor
# export CUDA_VISIBLE_DEVICES="4"
python inference.py \
   --checkpoints ./ckpt/checkpoint-740000/ \
   --data_path ./dataset/bm40case2msa.pkl \
   --do_predict \
   --mode orphan \
   -num 16 \
   -t 1 \
   --repetition_penalty 1.0 \

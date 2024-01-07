#!/usr/bin/env python

import af2_features
import os, sys, time, pickle, gzip, argparse
import matplotlib.pyplot as plt
import seaborn as sns
from IPyRSSA import General, Colors
import time

exists = os.path.exists
join   = os.path.join

parser = argparse.ArgumentParser(description='Run Jax AF2')
parser.add_argument('input_content',  type=str,   default=None, help="Input file or seq")
parser.add_argument('out_prefix',   type=str,     default=None, help="Input output prefix")
parser.add_argument('--run-single', action='store_true',   help="Run single seq version")
parser.add_argument('--model', type=str, default='model_3_ptm', choices=[f'model_{i}_ptm' for i in range(1, 6)],  help="AF2 models")
args = parser.parse_args()

def read_input(input_content:str):
    """
    Read input query

    Parameters
    ---------------
    input_content: 
        - xxx.fa / xxx.fasta: Sequence with fasta format
        - xxx.txt: MSA sequences with .txt suffix
        - xxx.pkl.gz / xxx.pkl: AF2 features file
        - xxx.lst: batch file. Each line represent a query
        - protein sequence

    Return
    ---------------
    q_seqs: List of query sequences
    fts: List of AF2 feature dict
    """
    q_seqs, fts = [], []
    if input_content.endswith(('.fa', '.fasta')):
        name2seq = General.load_fasta(input_content)
        assert len(name2seq) == 1
        q_seq = list(name2seq.values())[0]
        start_search = time.time()
        ft    = af2_features.query_or_process_MSAFt(q_seq, False, None, None, True)
        print(f"MSA search time: {time.time() - start_search}", flush=True)
        q_seqs.append(q_seq)
        fts.append(ft)
    elif input_content.endswith('.txt'):
        msa   = [ line.strip().split()[0] for line in open(input_content) if len(line) >= 15 ]
        q_seq = msa[0]
        start_construct = time.time()
        ft    = af2_features.construct_MSAFt_from_msa(q_seq, msa)
        print(f"MSA construction time: {time.time() - start_construct}", flush=True)
        q_seqs.append(q_seq)
        fts.append(ft)
    elif input_content.endswith(('.pkl.gz', '.pkl')):
        ft    = af2_features._load_pickle(input_content)
        q_seq = af2_features.aatype2seq(ft['aatype'])
        q_seqs.append(q_seq)
        fts.append(ft)
    # elif input_content.endswith('.lst'):
    #     contents = [ line.strip() for line in open(input_content) if line.strip() != "" ]
    #     for idx, content in enumerate(contents):
    #         cur_q_seqs, cur_fts = read_input(content)
    #         q_seqs += cur_q_seqs
    #         fts    += cur_fts
    elif len(set(input_content) - set(af2_features.restypes_with_x)) == 0:
        q_seq = input_content
        ft = af2_features.query_or_process_MSAFt(q_seq, False, None, None, True)
        q_seqs.append(q_seq)
        fts.append(ft)
    else:
        raise RuntimeError(f"Unknow input: {input_content}")
    return q_seqs, fts

start_time = time.time()
contents = [ line.strip() for line in open(args.input_content) if line.strip() != "" ]
filenames = [ content.split('/')[-1].split('.')[0] for content in contents ]
assert len(contents) == len(filenames)
for idx, content in enumerate(contents):
    round_time = time.time()
    out_pdb        = f'{args.out_prefix}_{filenames[idx]}.pdb'
    out_single_pdb = f'{args.out_prefix}_single_{filenames[idx]}.pdb'
    if (args.run_single and exists(out_single_pdb)) or (not args.run_single and exists(out_pdb)):
        continue
    q_seqs, fts = read_input(content)
    assert len(q_seqs) == len(fts) == 1
    q_seq = q_seqs[0]
    print(len(q_seq), flush=True)
    ft = fts[0]
    if args.run_single and (not exists(out_single_pdb) or not exists(out_single_png)):
        print(f"Running single model for {out_single_pdb}", flush=True)
        ft_single = af2_features.construct_MSAFt_from_msa(q_seq, [q_seq] * 128)
        res   = af2_features.run_af2_PDBpred(ft_single, args.model, num_ensemble=1, num_recycle=3, subbatch_size=64)
        prot  = af2_features.runner2prot(ft_single, res)
        ptm   = res['ptm'].item()
        plddt = prot.b_factors[:,1].mean()
        af2_features.save_prot_as_pdb(prot, out_single_pdb, full_seq=q_seq, remark_lines=[f'pTM={ptm:.3f}', f"pLDDT={plddt:.3f}"])
        # af2_features.plot_pAE(res['predicted_aligned_error'], out_single_png)
        print(f"total time used {time.time() - start_time} sec", flush=True)
        print(f"round time used {time.time() - round_time} sec", flush=True)
    
    else:
        if not exists(out_pdb) or not exists(out_png):
            print(f"Running model for {out_pdb}", flush=True)
            res   = af2_features.run_af2_PDBpred(ft, args.model, num_ensemble=1, num_recycle=3, subbatch_size=64)
            prot  = af2_features.runner2prot(ft, res)
            ptm   = res['ptm'].item()
            plddt = prot.b_factors[:,1].mean()
            af2_features.save_prot_as_pdb(prot, out_pdb, full_seq=q_seq, remark_lines=[f'pTM={ptm:.3f}', f"pLDDT={plddt:.3f}"])
            # af2_features.plot_pAE(res['predicted_aligned_error'], out_png)
            print(f"total time used {time.time() - start_time} sec", flush=True)
            print(f"round time used {time.time() - round_time} sec", flush=True)   
    




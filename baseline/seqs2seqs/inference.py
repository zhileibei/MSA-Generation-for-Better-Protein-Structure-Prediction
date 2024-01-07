
import json
from transformers import T5Tokenizer, T5Config
from model.msa_augmentor import MSAT5
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union
from data.utils_inference import DataCollatorForMSA
import torch
import torch
import os 
import logging
import datetime
import torch.nn.functional as F
import argparse
from data.msa_dataset import MSADataSet

logger = logging.getLogger(__name__)
logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d %H:%M:%S",
        level=logging.INFO,
    )
  
logger.setLevel(logging.INFO)


def msa_generate(args,model,dataset,msa_collator,tokenizer):
    """
    Generate msa for given dataset
    """
    with torch.no_grad():
        output_dir=os.path.join(args.output_dir,args.dataset,"small",f"N_{args.output_num}")
        args_dict = vars(args)
        os.makedirs(output_dir,exist_ok=True)
        with open(os.path.join(output_dir,'params.json'), 'w') as f:
            json.dump(args_dict, f, indent=4)
        logger.info('generate src files-num: {}'.format(len(dataset)))
        for a3m_data in dataset:
            # breakpoint()
            msa_name=a3m_data['msa_name']
            msa:List[Tuple[str,str]]=a3m_data['msa']
            src_ids=msa_collator.msa_batch_convert(msa).to('cuda:0')
            _,original_seq_num,original_seq_len=src_ids.size()
            for trial in range(args.trials_times):
                msa_output_dir=os.path.join(output_dir,msa_name)
                os.makedirs(msa_output_dir,exist_ok=True)
                a3m_file_name=os.path.join(msa_output_dir,f"generation_2.txt")
                if os.path.exists(a3m_file_name):
                    logger.info(f'File {a3m_file_name} already exists, skip')
                    continue               
                output=model.generate(src_ids,do_sample=True,top_k=5,top_p=0.95,repetition_penalty=args.repetition_penalty, \
                                    max_length=original_seq_len+1,gen_seq_num=args.output_num) 
                
                generate_seq=[tokenizer.decode(seq_token,skip_special_tokens=True).replace(' ','') for seq_token in output[0]]
                generate_seq=list(filter(lambda x: len(set(x))>5, generate_seq)) # filter our sequences with all gap '-'
                
                with open(a3m_file_name,'w') as fw:
                    generate_msa_list=[]
        
                    for original_seq in msa:
                        # generate_msa_list.append('>'+original_seq[0])
                        generate_msa_list.append(original_seq[1])
                    for i,seq in enumerate(generate_seq):
                        # seq_name='MSAT5_Generate_condition_on_{}_seq_from_{}_{}'.format(src_ids.size(1),msa_name,i)
                        # generate_msa_list.append('>'+seq_name)
                        generate_msa_list.append(seq)
                        
            

                    fw.write("\n".join(generate_msa_list))
                    logger.info(f'Generate successful for {msa_name} trial: {trial}')



def inference(args):
    
    config=T5Config.from_pretrained('./config/')
    tokenizer=T5Tokenizer.from_pretrained('./config/')
    msadata_collator=DataCollatorForMSA(tokenizer,max_len=512)
    if args.checkpoints:
        logger.info("loading model from {}".format(args.checkpoints))
        model=MSAT5.from_pretrained(args.checkpoints).to('cuda:0')
    else:
        logger.warning("Loading a random model")
        model=MSAT5(config).to('cuda:0')
    logger.info("parameter num {}".format(sum(p.numel() for p in model.parameters())))
    dataset=MSADataSet(data_dir=args.data_path,only_poor_msa=20)
    msa_generate(args,model=model,msa_collator=msadata_collator,
                dataset=dataset,tokenizer=tokenizer) 
        

def parsing_arguments():
    parser=argparse.ArgumentParser()
    # general params
    parser.add_argument('--do_train',action='store_true',help="whether further fine-tune")
    parser.add_argument('--do_predict',action='store_true',help="only create new seqs")
    parser.add_argument('--checkpoints',type=str,\
                        help="the folder path of model checkpoints, e.g '/msat5-base/checkpoint-740000'")
    parser.add_argument('--data_path',type=str, \
                        help="the folder path of poor data eg. './dataset/casp15/cfdb/'")
    parser.add_argument('-o','--output_dir',type=str,default="./output/",help="the folder path of output files")

    # Generation parmas
    parser.add_argument('--mode',type=str,choices=['orphan','artificial'],required=True,help="whether task is real world orpha enhancement or artificial enhancement")
    parser.add_argument('--repetition_penalty',type=float,default=1.2,help="repetition penalty for generation")
    parser.add_argument('-num','--output_num',type=int,default=1,help="times of generated quality compared to original msa x1 x3 x5")
    parser.add_argument('-t','--trials_times',type=int,default=5)    
    args=parser.parse_args()
    if 'casp14' in args.data_path:
        args.dataset='casp14'
    elif 'casp15' in args.data_path:
        args.dataset='casp15'
    else:
        args.dataset='bm'
    assert not (args.do_train and args.do_predict), "select one mode from train and predict"
    return args
    
if __name__=="__main__":
    args=parsing_arguments()
    args_dict = vars(args)
    args_str = json.dumps(args_dict, indent=4, sort_keys=True)
    logger.info('paramerters：%s', args_str)
    inference(args)
    

  
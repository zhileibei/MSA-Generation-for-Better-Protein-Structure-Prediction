# MSA-Generation-for-Better-Protein-Structure-Prediction
清华大学ANN-2023课程大作业项目

## 项目结构

```
.
├── README.md
├── analysis
│   ├── README.md
│   ├── analysis.ipynb
│   └── calc_time.py
├── baseline
│   ├── README.md
│   ├── evogen
│   │   ├── README.md
│   │   ├── evogen.py
│   │   └── main.py
│   └── seqs2seqs
│       ├── README.md
│       ├── inference.py
│       ├── inference.sh
│       └── msa_dataset.py
└── evaluation
    ├── README.md
    ├── get_af2_MSA.py
    ├── get_af2_ft.py
    ├── pipeline
    │   ├── convert_to_af2_files_dynamic.py
    │   ├── create_batch.py
    │   ├── extract_tmscore.py
    │   ├── gen_af2_cmd.py
    │   ├── gen_tmscore_cmd.py
    │   ├── process_msa_output.py
    │   └── run_all.py
    └── run_af2.py
```

-  baseline文件夹下是在baseline模型源代码基础上进行修改和替换的代码，包括evogen和seqs2seqs两个模型。
- evaluation文件夹下是实用AlphaFold2对MSA生成质量进行评估的代码。
- analysis文件夹下是数据分析文件，包括分析结果的生成、分析结果的可视化等。

详见各级子目录README.md文件。
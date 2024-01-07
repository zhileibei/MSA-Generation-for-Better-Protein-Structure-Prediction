### MSA Evaluation with AlphaFold2

通过比较使用MSA后，AlphaFold2对主序列的结构预测准确率相比不使用MSA提升了多少，来作为MSA生成质量的评估手段。

#### 流程
见pipeline子目录下各文件：

1. process_msa_output.py从模型生成的原始序列中提取出主序列和MSA，并计算MSA与主序列的序列同一性。
2. convert_to_af2_files_dynamic.py将MSA生成结果根据序列同一性进行采样，并转换成下游run_af2.py所需的输入格式。
3. create_batch.py将转换后的输入格式进行打包，以批量输入run_af2.py进行结构预测。
4. gen_af2_cmd.py根据批量输入文件生成运行run_af2.py的bash脚本。
5. run_all.py同时启动8个子进程运行指定目录下的bash脚本。
6. gen_tmscore_cmd.py根据run_af2.py的输出结果生成计算TM-score的bash脚本。
7. 手动运行计算TM-score的bash脚本，结果被自动写入同一目录下的AF2_TMscore.txt。
8. extract_tmscore.py从AF2_TMscore.txt中提取TM-score并生成结果文件。

#### 其他文件
- get_af2_MSA.py用于获得AlphaFold2搜索出的所有自然界MSA，用于分析生成的MSA与自然界MSA的相似性。
- get_af2_ft.py用于获得AlphaFold2搜索出的所有自然界MSA的features.pkl，用于baseline模型evogen的输入。同时根据我们的模型的实验设置进行seqs2seqs输入数据的生成。
- run_af2.py用于运行AlphaFold2进行结构预测。
### baseline：前人工作结果复现

我们对报告中相关工作部分提到的两篇探索MSA生成的工作进行结果复现。为了使不同模型之间的对比尽量公平，我们采用了相同的流程进行推理（比如都生成16条MSA、采用同样的采样策略等），这或许会与baseline模型原论文中汇报结果的处理流程有所不同。我们将所修改的代码文件放在各模型子目录下。

1. evogen：Unsupervisedly Prompting AlphaFold2 for Accurate Few-Shot Protein Structure Prediction

2. seqs2seqs：MSA generation with seqs2seqs pretraining: Advancing protein structure predictions
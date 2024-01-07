### Seqs2seqs Baseline

源代码：https://github.com/lezhang7/MSA-Augmentor.git

我们对源代码进行了一些修改，以保持各个baseline模型与我们模型的实验流程一致。为此我们修改并替换了seqs2seqs源代码中的下列文件：

- data/msa_dataset.py
- scripts/inference.sh
- inference.py

运行方式：

```bash
bash scripts/inference.sh
```
# PsiRec

### Introduction

This is the implementation of *PsiRec* as described in the paper:<br>
> Pseudo-Implicit Feedback for Alleviating Data Sparsity in Top-K Recommendation.<br>
> IEEE Conference on Data Mining, 2018.<br>
> Yun He, Haochen Chen, Ziwei Zhu and James Caverlee.<br>

The *PsiRec* algorithm generates pseudo-implicit feedback with indirect user-item relationships to enrich the original extreme datasets. This algorithm focuses on alleviating the data sparsity problem in top-K recommendation for implicit feedback datasets.

### Usage
PsiRec learns the user preference from training datasets and then ranks the items for the users in testing datasets.

#### Input
The input of PsiRec is the set of interactions between users and items from the training dataset:

``userId itemId 1.0``

1.0 means the user purchased the item.

#### Output
The output are the evaluation results comparing the ranked items of PsiRec and the groundtruth from the testing dataset. An example is presented as follows:

```
precision@5: 0.00935503812075
recall@5: 0.0312448221345
precision@10: 0.00683597774572
recall@10: 0.0451534507274
```

#### Run
./PsiRec.py --train_file filePath --test_file filePath --walk_length 80 --num_walks 10

#### Parameters
- -train_file, the training dataset file;
- -test_file, the testing dataset file (or validation dataset file);
- -walk_length, the length of a random walk; the default is 80;
- -num_walks, the number of random walks visiting each user and item; the default is 10;
- -window_size, the context size for sampling the indirect user-item pairs; the default is 3;
- -user_number, the number of users in the dataset;
- -item_number, the number of items in the dataset;
- -train_epoch, the iterations of ALS matrix factorization; the default is 25;
- -lambda_value, the regularization value for ALS matrix factorization; the default is 0.25.
- -latent_factors, the number of latent factors of ALS matrix factorization; the default is 100;
- -validation, the Boolean variable to decide if do the validation on the validation dataset; the default is 0.

### Files in folder

#### PsiRec
- -PsiRec.py, the main function of PsiRec;
- -randomWalks.py, the file to generate random walks from the user-item bigraph;
- -SPPMI.py, the file to calculate Shifted Positive Pointwise Mutual Information (SPPMI) value as the confidence for each pseudo-implicit feedback;
- -alsMF.py, the file to apply latent factors model to predict the item lists for each user based on the dataset enriched by PsiRec;
- -evaludation.py, the file to do the evaluation;

#### Data
- -preProcessData.py, the file to preprocess the raw datasets, including transferring explicit datasets to implicit datasets and split the dataset into three parts: training, testing and validation;
- -DataInPaper, the datasets exactly the same in our paper, which can be used directly by PsiRec.py;
- -rawData, the raw datasets are too large to be handled here, but you can download according the URLs presented in our paper;
- -preProcessedData, the preprocessed datasets, which can be used directly by PsiRec.py;

### Citation
Pending.

### Acknowledgement
The technique of randomWalks.py is learned from https://github.com/aditya-grover/node2vec. Th frsit author is Aditya Grover from Standfor University. Thanks to them!






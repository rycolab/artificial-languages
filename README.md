# Examining the Inductive Bias of Neural Language Models with Artificial Languages

## Paper

This repository contains code accompanying ['Examining the Inductive Bias of Neural Language Models with Artificial Languages'](https://aclanthology.org/2021.acl-long.38/) by Jennifer C. White and Ryan Cotterell (ACL 2021).

## Generating Grammars From Choice Points

`base-grammar.gr` contains a simple base grammar with 6 possible constructions whose orders may be changed between head-final and head-initial orderings. Each of the productions that would need to be reversed to make this possible is marked with a number. Productions that are part of one construction share the same number.

By running `gen_data.sh`, splits will be generated containing matched sample sentences that differ only in their constituent ordering and cover all possible combinations of these swappable orderings.

In the names of the generated folder of the form XXXXXX, each of the swappable orderings (labelled i) is represented by a 0 (indicating head-final ordering) or a 1 (indicating head-initial) in the ith position.

The orderings are labelled as follows:

* 1 - Position of verb within a sentence
* 2 - Position of noun within a verb phrase
* 3 - Position of complementizer in a complement
* 4 - Ordering of prepositional phrase
* 5 - Position of adjective in a noun phrase
* 6 - Position of relativizer when making a relative clause

## Training Language Models

[Fairseq](https://github.com/pytorch/fairseq) is required to train the models used in the paper.

The scripts used to extract scores and collate results also assume that results are output in the form used by Fairseq.

`train_lm_transformer.sh` and `train_lm_lstm.sh` will train a fairseq transformer and LSTM, respectively, on the grammar and split that they are passed.

`python run_all_jobs.py` will cycle through all grammars and all splits and train a transformer and an LSTM on each. Using `--submission_command`, a job submission command for an HPC system can be passed in, so that each of these models is submitted to the desired HPC system as a separate job (this may require modification depending on the system being used.

## Collating Results

After all models are finished training, run
 ```bash
 python compile_results.py -f trans-results/ -o trans-results.csv && python compile_results.py -f lstm-results/ -o lstm-results.csv
 ```
to generate CSVs containing mean and standard deviations of perplexity across all grammars.

And run 
```bash
python combine_sent_scores.py -f trans_sentence_scores/ -O compiled_trans_scores/ && python combine_sent_scores.py -f lstm_sentence_scores/ -O compiled_lstm_scores/ 
```
to combine sentence scores from all splits into one file per grammar.

## Analysis of Results

Run
```bash
python results_analysis/permutation_test.py -f compiled_trans_scores/  -O transformer && python results_analysis/permutation_test.py -f compiled_lstm_scores/  -O lstm
```
to generate a CSV showing which grammars exhibit a statistically significant difference in performance.

Run
```bash
python results_analysis/mixed_model.py -f compiled_trans_scores/ -o transformer_mixed.csv -i True && python results_analysis/mixed_model.py -f compiled_lstm_scores/ -o lstm_mixed.csv -i True
```
to model the results using mixed effecs models. 

## Requirements

Fairseq, pandas, numpy, statsmodels

## Citation

```bash
@inproceedings{white-cotterell-2021-examining,
    title = "Examining the Inductive Bias of Neural Language Models with Artificial Languages",
    author = "White, Jennifer C.  and
      Cotterell, Ryan",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.38",
    doi = "10.18653/v1/2021.acl-long.38",
    pages = "454--463",
    abstract = "Since language models are used to model a wide variety of languages, it is natural to ask whether the neural architectures used for the task have inductive biases towards modeling particular types of languages. Investigation of these biases has proved complicated due to the many variables that appear in the experimental setup. Languages vary in many typological dimensions, and it is difficult to single out one or two to investigate without the others acting as confounders. We propose a novel method for investigating the inductive biases of language models using artificial languages. These languages are constructed to allow us to create parallel corpora across languages that differ only in the typological feature being investigated, such as word order. We then use them to train and test language models. This constitutes a fully controlled causal framework, and demonstrates how grammar engineering can serve as a useful tool for analyzing neural models. Using this method, we find that commonly used neural architectures exhibit different inductive biases: LSTMs display little preference with respect to word ordering, while transformers display a clear preference for some orderings over others. Further, we find that neither the inductive bias of the LSTM nor that of the transformer appear to reflect any tendencies that we see in attested natural languages.",
}
```

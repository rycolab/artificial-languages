python sample_sentences.py -g base-grammar.gr -n 100000 -O . -b True
python permute_sentences.py -s sample_base-grammar.txt -O permuted_samples/ 
python make_splits.py -S permuted_samples/ -O permuted_splits/
import os
import random
import argparse

def create_splits(sample_file, num_splits, train, test, dev, output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)  
    sentence_file = open(sample_file, 'r')
    all_sentences = sentence_file.readlines()
    num_all_sent = len(all_sentences)
    grammar_name = sample_file[:-4].split("_")[-1]
    if not os.path.exists(os.path.join(output_folder, grammar_name)):
        os.mkdir(os.path.join(output_folder, grammar_name))
    grammar_output = os.path.join(output_folder, grammar_name)
    for i in range(num_splits):
        start = int(i * (1/num_splits) * num_all_sent)
        end = int((i+1) * (1/num_splits) * num_all_sent)
        sentences = all_sentences[start:end]
        num_sent = len(sentences)
        trn_output = open(os.path.join(grammar_output, str(i) + ".trn"), 'w')
        tst_output = open(os.path.join(grammar_output, str(i) + ".tst"), 'w')
        dev_output = open(os.path.join(grammar_output, str(i) + ".dev"), 'w')
        trn_split = sentences[:int(train*num_sent)]
        tst_split = sentences[int(train*num_sent):int((train + test)*num_sent)]
        dev_split = sentences[int((train + test)*num_sent):]
        for s in trn_split:
            trn_output.write(s)
        for s in tst_split:
            tst_output.write(s)
        for s in dev_split:
            dev_output.write(s)

parser = argparse.ArgumentParser(
    description="Divide generated sentences into splits")

parser.add_argument("-s", "--sample_file", type=str, default='',
    help="Path to sample file")
parser.add_argument("-S", "--sample_folder", type=str, default='',
    help="Path to folder containing multiple sample files")
parser.add_argument("-O", "--output_folder", type=str, 
    help="Location of output files")
parser.add_argument("-tr", "--train", type=float, default=0.8, 
    help="Train proportion")
parser.add_argument("-ts", "--test", type=float, default=0.1, 
    help="Test proportion")
parser.add_argument("-dv", "--dev", type=float, default=0.1, 
    help="Dev proportion")
parser.add_argument("-n", "--num_splits", type=int, default=10, 
    help="Number of splits")

args = parser.parse_args()

assert(args.train + args.test + args.dev == 1.0)

if args.sample_file == '' and args.sample_folder == '':
    print("Please provide sample files")
elif args.sample_file != '' and args.sample_folder != '':
    print("Please provide either a single file OR a folder containing sample"
        " files")
elif args.sample_file != '':
    create_splits(args.sample_file, args.num_splits, args.train, args.test, 
        args.dev, args.output_folder)
elif args.sample_folder != '':
    sample_files = [f for f in os.listdir(
        args.sample_folder) if f.endswith('.txt')]
    for s in sample_files:
        create_splits(os.path.join(args.sample_folder, s), args.num_splits, 
            args.train, args.test, args.dev, args.output_folder)

        

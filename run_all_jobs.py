import subprocess
import argparse

parser = argparse.ArgumentParser(description="Run all jobs")

parser.add_argument("-s", "--num_splits", type=int, default=10,
    help="Number of splits")
parser.add_argument("-n", "--num_choices", type=int, default=6,
    help="Number of choice points")
parser.add_argument("--submission_command", type=str, default="", 
    help="Command used to submit jobs to HPC system")

args = parser.parse_args()

for i in range(2 ** args.num_choices):
    grammar = format(i, '0' + str(args.num_choices) + 'b')[::-1]
    for j in range(args.num_splits):
        subprocess.call(args.submission_command 
            + " ./conlang-grammar/train_lm_transformer.sh " 
            + ' '.join([str(grammar), str(j)]), shell=True)
        subprocess.call(args.submission_command 
            + " ./conlang-grammar/train_lm_lstm.sh " 
            + ' '.join([str(grammar), str(j)]), shell=True)
import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Compile sentence scores across "
    "splits into one file for each grammar")

parser.add_argument("-f", "--file_location", type=str, required=True, 
    help="Path to folder containing files")

parser.add_argument("-O", "--output_folder", type=str, required=True,
    help="Location of output folder")

args = parser.parse_args()

for i in range(64):
    grammar = format(i, '06b')[::-1]
    score_files = [os.path.join(args.file_location, grammar, 
        f) for f in os.listdir(os.path.join(args.file_location, 
            grammar)) if f.endswith('.txt')]
    score_files.sort(key=lambda f: f.split("/")[-1].split(".")[0])
    scores = []
    for f in score_files:
        file = open(f, 'r')
        file_scores = file.readlines()
        scores += file_scores
    if not os.path.exists(os.path.join(args.output_folder)):
        os.mkdir(os.path.join(args.output_folder))
    output_file = open(os.path.join(args.output_folder, 
        grammar + "_scores.txt"), 'w')
    for s in scores:
        output_file.write(s)
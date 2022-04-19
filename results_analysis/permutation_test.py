import argparse
import os
import random
import csv

def permutation_test(v1, v2, s):
    assert(len(v1) == len(v2))
    diff_av = abs(sum([(v1[i] - v2[i]) for i in range(len(v1))])/len(v1))
    swapped_av = 0
    for i in range(s):
        diff_tot = 0
        for j in range(len(v1)):
            diff = v1[j] - v2[j]
            flip = random.randint(0,1)
            if flip:
                diff = -diff
            diff_tot += diff
        swapped_diff_av = abs(diff_tot/len(v1))
        if swapped_diff_av >= diff_av:
            swapped_av += 1
    return swapped_av/s

parser = argparse.ArgumentParser(description="Perform permutation tests")

parser.add_argument("-f", "--file_location", type=str, default='', 
    help="Path to folder containing files")

parser.add_argument("-s", "--number_samples", type=int, default=10000, 
    help="Number of permutations to sample")

parser.add_argument("-l", "--file_list", type=str, default='', 
    help="Two files, separated by commas, to compare")

parser.add_argument("-O", "--output_folder", type=str, default='',
    help="Location of output file")

args = parser.parse_args()

if len(args.file_location) > 0:
    if len(args.output_folder) > 0:
        output_file = open(os.path.join(args.output_folder, 
            'perm_test_results.csv'), 'w')
        fieldnames = ['Grammar'] + [format(i, '06b') for i in range(64)]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
    else:
        writer = None

    for i in range(64):
        grammar_i = format(i, '06b')
        file_i = open(os.path.join(args.file_location, 
            grammar_i + "_scores.txt"), 'r')
        lines_i = file_i.readlines()
        scores_i = [float(l.strip("\n")) for l in lines_i]
        i_dict = {"Grammar":grammar_i}
        for j in range(i+1, 64):
            grammar_j = format(j, '06b')
            file_j = open(os.path.join(args.file_location, 
                grammar_j + "_scores.txt"), 'r')
            lines_j = file_j.readlines()
            scores_j = [float(l.strip("\n")) for l in lines_j]
            if permutation_test(scores_i, scores_j, args.number_samples) < 0.05:
                if (-1 * sum(scores_j)/len(scores_j) 
                    > -1 * sum(scores_i)/len(scores_i)):
                    print("SIGNIFICANT:", grammar_j, ">", grammar_i)
                    if len(args.output_folder) > 0:
                        i_dict[grammar_j] = "<"
                else:
                    print("SIGNIFICANT:", grammar_i, ">", grammar_j)
                    if len(args.output_folder) > 0:
                        i_dict[grammar_j] = ">"
            else:
                if len(args.output_folder) > 0:
                    i_dict[grammar_j] = "x"
        if len(args.output_folder) > 0:
            writer.write(i_dict)
elif len(args.file_list) > 0 and len(args.file_list.split(",")) == 2:
    filename_a = args.file_list.split(",")[0]
    filename_b = args.file_list.split(",")[1]
    lines_a = open(filename_a, 'r').readlines()
    lines_b = open(filename_b, 'r').readlines()
    scores_a = [float(l.strip("\n")) for l in lines_a]
    scores_b = [float(l.strip("\n")) for l in lines_b]
    print(permutation_test(scores_b, scores_b, args.number_samples))
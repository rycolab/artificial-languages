import csv
import argparse
import os
import math

def get_perplexity(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	final_line = lines[-1].strip('\n')
	return float(final_line.split(" ")[-1])

def calc_sd(vals):
	mean = calc_mean(vals)
	return math.sqrt(sum([(x - mean)**2 for x in vals])/len(vals))

def calc_mean(vals):
	return sum(vals)/len(vals)

parser = argparse.ArgumentParser(description="Calculate mean and SD of "
	"perplexity for dev and test for each grammar")

parser.add_argument("-f", "--folder", type=str, required=True,
    help="Location of results file")

parser.add_argument("-o", "--output", type=str, required=True, 
	help="Location to save output")

args = parser.parse_args()

results_files = [os.path.join(args.folder, f) for f in os.listdir(
	args.folder) if f.endswith('.txt')]
perplexity_dict = {}
for res in results_files:
	grammar, split, test_dev, _ = res.split("/")[-1].split(".")
	if grammar not in perplexity_dict.keys():
		perplexity_dict[grammar] = {}
	if test_dev not in perplexity_dict[grammar].keys():
		perplexity_dict[grammar][test_dev] = []
	perplexity_dict[grammar][test_dev].append(get_perplexity(res))

output_file = open(args.output, 'w')
fieldnames = ['grammar', 'dev_av', 'dev_sd', 'tst_av', 'tst_sd']
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()
for i in range(64):
	grammar = format(i, '06b')
	writer.writerow({'grammar':grammar, 
		'dev_av':calc_mean(perplexity_dict[grammar]['dev']),
		'dev_sd':calc_sd(perplexity_dict[grammar]['dev']),
		'tst_av':calc_mean(perplexity_dict[grammar]['test']),
		'tst_sd':calc_sd(perplexity_dict[grammar]['test'])
		})

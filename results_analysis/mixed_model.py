import argparse
import os
import sys
import pandas as pd
import numpy as np
from statsmodels.regression.mixed_linear_model import MixedLM

def read_scores_from_file(filename):
    score_file = open(filename, 'r')
    scores = score_file.readlines()
    indxd_scores = []
    for i in range(len(scores)):
        indxd_scores.append((i, -1.0*float(scores[i].strip("\n"))))
    return indxd_scores

def get_cross_interactions(attribs):
    cross = []
    for i in range(len(attribs)):
        for j in range(i + 1, len(attribs)):
            cross.append(attribs[i] + "_" + attribs[j])
    return cross

def get_dataframe(file_location, output, attribs):
    columns = ['sent_id', 'score'] + attribs
    results_df = pd.DataFrame(columns=columns)
    print(results_df.head())

    score_files = [os.path.join(file_location, f) for f in os.listdir(
        os.path.join(file_location)) if f.endswith('.txt')]

    for f in score_files:
        scores = read_scores_from_file(f)
        grammar_name = f.split("/")[-1].split("_")[0]
        attrib_vals = []
        for c in grammar_name:
            if c == '0':
                attrib_vals.append(-1.0)
            elif c == '1':
                attrib_vals.append(1.0)
        for s in scores:
            to_append = {'sent_id':s[0], 'score':s[1]}
            for i in range(len(attribs)):
                to_append[attribs[i]] = attrib_vals[i]
            results_df = results_df.append(to_append, ignore_index=True)

    results_df = results_df.astype({'sent_id':'int64'})
    if len(output) > 0:
        results_df.to_csv(output, index=False)
    return results_df

parser = argparse.ArgumentParser(
    description="Perform analysis with mixed effects model")

parser.add_argument("-f", "--file_location", type=str, default='', 
    help="Path to folder containing files")

parser.add_argument("-c", "--csv_location", type=str, default='', 
    help="Path to csv to load")

parser.add_argument("-o", "--output_csv", type=str, default='', 
    help="Location to save CSV")

parser.add_argument("-i", "--include_interactions", type=bool, default=False, 
    help="Whether interaction terms are included")

args = parser.parse_args()

attribs = ['S','VP','comp', 'PP', 'NP', 'rel']

if len(args.file_location) > 0 and len(args.csv_location) > 0:
    print("Error: Either provide CSV or score files, not both")
    results_df = None
elif len(args.file_location) > 0:
    results_df = get_dataframe(args.file_location, args.output_csv, 
        attribs)
elif len(args.csv_location) > 0:
    results_df = pd.read_csv(args.csv_location)
else:
    print("Error: Provide either CSV or score files")
    results_df = None

if args.include_interactions:
    cross_attribs = get_cross_interactions(attribs)
    for cross in cross_attribs:
        attrib1, attrib2 = cross.split("_")
        new_column = []
        for index, row in results_df.iterrows():
            new_column.append(row[attrib1] * row[attrib2])
        results_df[cross] = new_column

fml = "score ~ "
if args.include_interactions:
    all_attribs = attribs + cross_attribs
else:
    all_attribs = attribs
for a in all_attribs:
    fml += a + "+"

fml = fml.strip("+")

mod_lme = MixedLM.from_formula(fml, groups=results_df["sent_id"], 
    data=results_df)
mod_lme = mod_lme.fit()

print(mod_lme.summary())
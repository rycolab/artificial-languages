import argparse
import os
import sys
import random
import copy

def flip_as_needed(i, sentence):
    to_flip = [j + 1 for j in range(6) if (i >> j) & 1 == 1]
    s_split = sentence.split(" ")
    for j in range(len(s_split)):
        if s_split[j][0].isnumeric():
            if int(s_split[j][0]) in to_flip:
                reversed_end = reversed_children(s_split[j+1:])
                s_split = s_split[:j+1] + reversed_end
        else:
            continue
    return ' '.join(s_split).strip("\n")

def reversed_children(sentence_part):
    children = []
    bracket_stack = []
    L_brack = '('
    R_brack = ')'
    children_end = -1
    for i in range(len(sentence_part)):
        s = sentence_part[i]
        if s == L_brack:
            bracket_stack.append((L_brack, i))
        elif s == R_brack:
            if len(bracket_stack) > 0:
                if bracket_stack[-1][0] == L_brack:
                    opening = bracket_stack.pop()
                    if len(bracket_stack) == 0:
                        children.append(sentence_part[opening[1]:i+1])
            else:
                children_end = i - 1
                break
        else:
            continue
    children_reversed = []
    for c in children[::-1]:
        children_reversed += c
    return children_reversed + sentence_part[children_end:]

def remove_bracketing(s):
    new_s = []
    split_s = s.split(" ")
    i = 0
    while i < len(split_s):
        if split_s[i] == ")":
            i += 1
        elif split_s[i] == "(":
            i += 2
        else:
            new_s.append(split_s[i])
            i += 1
    new_s.append(".")
    return ' '.join(new_s)

def generate_sentence_file(i, sentences, output_file):
    output_f = open(output_file, 'w')
    for s in sentences:
        output_f.write(remove_bracketing(flip_as_needed(i, s)) + "\n")
    output_f.close()

parser = argparse.ArgumentParser(description="Generate variants of sentences"
    " based on base grammar")

parser.add_argument("-s", "--sentence_file", type=str, required=True, 
    help="Path to base sentence file")

parser.add_argument("-O", "--output_folder", type=str, required=True,
    help="Location of output folder")

args = parser.parse_args()

file = open(args.sentence_file, 'r')
sentences = file.readlines()

for i in range(64):
    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder) 
    grammar_name = format(i, '06b')[::-1]
    output_file = os.path.join(args.output_folder, 
        "sample_" + grammar_name + ".txt")
    generate_sentence_file(i, sentences, output_file)
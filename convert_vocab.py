import csv
import re
import random


def load_mapping(mappath):
    mapping = {}
    with open(mappath, 'rb') as f:
        reader = csv.reader(f)
        for line in reader:
            mapping[line[1]] = line[0]

    return mapping

def load_freqs(path):
    result = {}
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for token, freq in reader:
            token_type = re.sub(r'\d+', '', token)
            if token_type not in result:
                result[token_type] = []
            result[token_type].append((token, freq))

    # Sort the individual lists by frequrency
    final = {k: sorted(v, key=lambda x: x[1], reverse=True) for k, v in result.iteritems()}

    return final

def align(source_d, target_d, x=4):
    alignment = {}
    for token_type in source_d:
        source_freqs = source_d[token_type]
        target_freqs = target_d[token_type]

        for i, v in enumerate(source_freqs):

            # If there is a mate for this value in the target corpus
            # then pair the two.
            if i < len(target_freqs):
                alignment[v[0]] = target_freqs[i][0]
            # Otherwise pair it with one of the lowest x frequency tokens.
            else:
                alignment[v[0]] = target_freqs[-random.choice(list(range(1, x)))]

    return alignment





def convert_corpus(filepath, mapping, alignment, eos="xxEnD142xx xxBeGiN142xx"):
    general_corpus = ''
    with open(filepath, 'rb') as f:
        general_corpus = re.sub(eos, '.', f.read())

    corpus = []
    for token in general_corpus.split():
        if token == '.':
            # If the token is punctuation assign a random punctuation.
            corpus[-1] = corpus[-1] + random.choice(['.', '!', '?'])
        else:
            corpus.append(mapping[alignment[token]])

    output = ' '.join(corpus)
    output = re.sub(r' +', ' ', output)

    return output

def main(source_freq, target_freq, target_map, corpus_path, outpath):
    source_dict = load_freqs(source)
    target_dict = load_freqs(target)
    target_mapping = load_mapping(target_map)
    alignment = align(source_dict, target_dict)
    final_corpus = convert_corpus(corpus_path, target_mapping, alignment)
    with open(outpath, 'wb') as f:
        f.write(final_corpus)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extracts a distribution of sentence structures from a given corpus.')
    parser.add_argument(
        'source_freq', help='The filepath to the source frequencies', type=str)
    parser.add_argument(
        'target_freq', help='The filepath to the target frequencies', type=str)
    parser.add_argument(
        'target_map', help='The filepath to the target vocabulary mapping', type=str)
    parser.add_argument(
        'corpus_path', help='The filepath to the corpus to convert', type=str)
    parser.add_argument('output', help='The output path', type=str)

    args = parser.parse_args()
    main(args.source_freq, args.target_freq, args.source_map, args.target_map, args.output)
    exit()

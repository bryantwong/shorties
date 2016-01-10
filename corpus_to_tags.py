import nltk
import re


# Opens a file containing a corpus and cleans the text.
# <str> eos: string representing the end of a sentence in the corpus
# Returns a string containin'g the cleaned data.
def open_clean(filepath, eos=" xxEnD142xx xxBeGiN142xx "):
    text = ''
    with open(filepath, 'rb') as f:
        print 'Cleaning data...'
        # Clean non-ascii compatible characters.
        text = re.sub(r'[^\x00-\x7F]+', '', f.read())

    # Remove all non-standard punctuation.
    punct = r'["#$%&()*+,\-/:;<=>@\[\\\]^_`{|}~]'
    text = re.sub(punct, '', text)
    # Replace newlines with spaces.
    text = re.sub(r'\r\n', ' ', text)
    # Convert to lowercase.
    text = text.lower()
    # Replace punctuation with EOS character
    end, begin = eos.split()
    text = begin + re.sub(r'[.!?]', eos, text) + end
    # Remove any double-spaces.
    text = re.sub(r' +', ' ', text)

    return text


def count_frequencies(corpus):
    '''
    PARAMETERS:
        <str> corpus: The corpus for which to count the frequencies
    RETURNS:
        dict: A dictionary {token(str): frequency(int)}
    '''
    print 'Counting token frequencies...'
    freqs = dict()
    tokens = corpus.split()
    corpus_length = len(tokens)
    # Count the raw frequencies
    for t in tokens:
        freqs[t] = freqs.get(t, 0) + 1
    # Normalize by corpus size.
    normalized = {k: (float(v) / corpus_length) for k, v in freqs.iteritems()}
    return normalized


def generalize(tags, eos=" xxEnD142xx xxBeGiN142xx"):
    '''
    PARAMETERS:
        [(str, str)] tags: list of tagged tuples
        <str> eos: string representing the end of a sentence in the corpus
    RETURNS:
        <tuple> (general, mapping):
            -general is a string containing the original corpus with
             all tokens replaced by generics.
            -mapping is a dictionary containg the mapping from original
             tokens to generic tokens.
    '''
    print 'Mapping corpus to generics...'
    pos_counters = dict()
    mapping = dict()
    output = []
    eos_tokens = frozenset(eos.split())

    for t in tags:
        word, tag = t
        # If we haven't seen this word yet...
        if word in eos_tokens:
            mapping[word] = word
        elif word not in mapping:
            # Increment the index for the tag
            pos_counters[tag] = pos_counters.get(tag, 0) + 1
            mapping[word] = str(tag) + str(pos_counters[tag])

        output.append(mapping[word])

    return (' '.join(output), mapping)


def main(filepath, outpath):
    text = open_clean(filepath)
    tokens = nltk.word_tokenize(text)
    print 'Tagging corpus...'
    tags = nltk.pos_tag(tokens)
    general, mapping = generalize(tags)
    print 'Saving data...'
    with open(outpath + '/general.txt', 'wb') as f:
        f.write(general)
    with open(outpath + '/mapping.csv', 'wb') as f:
        f.write('\n'.join([k + ', ' + v for k, v in mapping.iteritems()]))
    freqs = count_frequencies(general)
    with open(outpath + '/freqs.csv', 'wb') as f:
        f.write('\n'.join([str(k) + ', ' + str(v) for k, v in freqs.iteritems()]))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extracts a distribution of sentence structures from a given corpus.')
    parser.add_argument('corpus', help='The filepath to the corpus', type=str)
    parser.add_argument('output', help='The output path', type=str)

    args = parser.parse_args()
    main(args.corpus, args.output)
    exit()

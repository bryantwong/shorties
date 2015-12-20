import nltk
import re


# Opens a file containing a corpus and cleans the text.
# Returns a string containing the cleaned data.
def open_clean(filepath):
    text = ''
    with open(filepath, 'rb') as f:
        print 'Cleaning data...'
        # Clean non-ascii compatible characters.
        text = re.sub(r'[^\x00-\x7F]+', u'', f.read())

        # Remove all non-standard punctuation.
        punct = r'["#$%&()*+,\-/:;<=>@\[\\\]^_`{|}~]'
        text = re.sub(punct, '', text)
        # Replace newlines with spaces.
        text = re.sub(r'\r\n', ' ', text)
        # Remove any double-spaces.
        text = re.sub(r' +', ' ', text)
        # Convert to lowercase.
        text = text.lower()

    return text


def generalize(tags):
    '''
    PARAMETERS:
        [(str, str)] tags: list of tagged tuples
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

    for t in tags:
        word, tag = t
        # If we haven't seen this word yet...
        if word not in mapping:
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
    with open(outpath+'/general.txt', 'wb') as f:
        f.write(general)
    with open(outpath+'/mapping.txt', 'wb') as f:
        f.write('\n'.join([k + ', ' + v for k, v in mapping.iteritems()]))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extracts a distribution of sentence structures from a given corpus.')
    parser.add_argument('corpus', help='The filepath to the corpus', type=str)
    parser.add_argument('output', help='The output path', type=str)

    args = parser.parse_args()
    main(args.corpus, args.output)
    exit()

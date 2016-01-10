import Algorithmia
import api_key
import re
from random import randint



def generate_trigrams(corpus, filepath):
	'''
	Generates a trained trigram model
	PARAMETERS:
		str[] corpus: array of strings generated from splitting
		              the original corpus. Needs beginning and
		              end tags in data
		<str> filepath: location that data is stored in Algorithmia
		                data API
	RETURNS:
        filepath: location that data is stored in Algorithmia data API
                  (as confirmation)
	'''
	with open(corpus, 'r') as myfile:
		data = myfile.read().replace('\n', '')
	data = data.replace("xxEnD142xx", "xxEnD142xx qq")
	data = data.split(" qq ")
	input = [data, "xxBeGiN142xx", "xxEnD142xx", filepath]
	client = Algorithmia.client(api_key.key)
	algo = client.algo('ngram/GenerateTrigramFrequencies/0.1.1')
	print "Trigram Frequency txt in data api, filepath is:"
	print algo.pipe(input)

def generate_sentence(filepath):
	'''
    Generates a sentence given a trained trigram model
    PARAMETERS:
    	<str> filepath: location that trained model is located
    					 in Algorithmia API
    RETURNS:
    	<str> output: a randomly generated sentence
	'''
	client = Algorithmia.client(api_key.key)
	input = [filepath, "xxBeGiN142xx", "xxEnD142xx"]
	algo = client.algo('ngram/RandomTextFromTrigram/0.1.1')
	print algo.pipe(input)

def main(filepath, outpath, length):
	story = ''
	client = Algorithmia.client(api_key.key)
	alg_path = "data://.algo/ngram/GenerateTrigramFrequencies/temp/trigrams.txt"
	generate_trigrams(filepath, alg_path)
	while len(re.findall(r'\w+', story)) < length:
		print "Generating new paragraph..."
		input = ["data://.algo/ngram/GenerateTrigramFrequencies/temp/trigrams.txt", "xxBeGiN142xx", "xxEnD142xx", (randint(1,9))]
		new_par = client.algo('/lizmrush/GenerateParagraphFromTrigram/0.1.2').pipe(input)
		if len(re.findall(r'\w+', story)) + len(re.findall(r'\w+', new_par)) > length:
			break
		story += new_par.strip()
		story += '\n\n'
		print "Word count:"
		print len(re.findall(r'\w+', story))

	with open(outpath, 'w') as f:
		f.write(story.encode('utf8'))

	f.close()

	print "Complete! Story written to " + outpath

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Generates sentences using a trigram model and the Algorithmia API')
    parser.add_argument('input', help='The filepath to to tokenized corpus', type=str)
    parser.add_argument('output', help='The output path', type=str)
    parser.add_argument('length', help = 'Max story length', type=int)

    args = parser.parse_args()
    main(args.input, args.output, args.length)
    exit()

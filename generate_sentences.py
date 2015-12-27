import Algorithmia


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
	input = [corpus, "xxBeGiN142xx", "xxEnD142xx", filepath]
	client = Algorithmia.client('simfAKlzXJA516uRJm37b8tT9b31')
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
	input = [filepath, "xxBeGiN142xx", "xxEnD142xx"]
	client = Algorithmia.client('simfAKlzXJA516uRJm37b8tT9b31')
	algo = client.algo('ngram/RandomTextFromTrigram/0.1.1')
	print algo.pipe(input)

def main():
	

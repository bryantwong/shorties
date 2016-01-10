# Author Mashup (for [Algorithmia Shorties Contest](https://github.com/algorithmiaio/shorties))
### by Bryant Wong and Logan Walls

Ever wondered what Plato's "Republic" would be like if James Joyce had written it? Or if Plato had written Joyce's "Dubliners?" Or maybe if Jane Austen had writen Joyce's "Ulysses?" (We just really like Joyce.) Our idea was to generate short stories that were mashups of any two authors (or two corpuses in general) by using one corpus to generate a sentence structure for the story, and the other corpus to provide vocabulary for the story to use.

## How it works ##
Using the scripts is a bit of a pain, since it's a bit hacked together, but if you want to try it out, feel free to clone the repo. You will need [nltk](https://github.com/nltk/nltk) as well as your own Algorithmia API key.

You want to run `corpus_to_tags.py` on both corpuses as this does our part of speech taggings, as well as generating counts for the frequencies of different part of speech.

Then, run `generate_sentences.py`. This heavily uses the Algorithmia API (namely [GenerateParagraphFromTrigram](https://algorithmia.com/algorithms/lizmrush/GenerateParagraphFromTrigram) and [GenerateTrigramFrequencies](https://algorithmia.com/algorithms/ngram/GenerateTrigramFrequencies)) to create a story that mimics the structure of one of the corpuses. Notice this story is written entirely in part of speech tags and isn't so fun to read.

Finally, run `convert_vocab.py`. This utilizes the mappings and frequency counts from both to pick the most commonly used words of each type in the second corpus and insert them into the structure created by the first corpus, making a mashup. Then, read your story and enjoy how nonsensical it is.

## Caveats ##
Yeah, it still doesn't work very well (some of it might be nltk's fault!). But to make your story more readible, avoid:
1. Mashing up authors from different eras. The structure and most common parts of speech from different eras tend to be very different and you get some very odd sentences. The mapping tends not to work so well in those cases.
2. Authors that use non-traditional words or non-traditional structures. Probably shouldn't have picked Joyce... At least we learned his structure and style is hard to emulate.

##Some sample works: ##
[Republic structure w/Dubliners vocabulary](https://github.com/bryantwong/shorties/blob/master/stories/republic_dubliners.txt)

[Dubliners structure w/Republic vocabulary](https://github.com/bryantwong/shorties/blob/master/stories/dubliners_republic.txt)

[Ulysses structure w/ Pride and Prejudice vocabulary](https://github.com/bryantwong/shorties/blob/master/stories/ulysses_pride_prejudice.txt)

Thanks and enjoy!

import argparse
import os
ENGLISH_WORD_DICT = '/usr/share/dict/words'

# https://www.aclweb.org/anthology/P11-1140.pdf
# splitting english compound words
def get_constituents_for_compound(word,english_word_dictionary):

    if len(word) <= 2:
        return []

    if '-' in word:
        return word.split('-')

    for i in range(2,len(word)-2):
        constituent_1 = word[0:i]
        constituent_2 = word[i:]

        if constituent_1 in english_word_dictionary and constituent_2 in english_word_dictionary:
            return  [constituent_1,constituent_2]
    return []


# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_vocab_file", help = "Vocab file from which constituent compound mapping will be extracted",required=True)
parser.add_argument("-l", "--language", help = "german or english",required=True)
parser.add_argument("-o","--output_mapping_file",help = "Mapping file for constituent and compounds",required=True)
# Read arguments from command line
args = parser.parse_args()

with open(args.input_vocab_file,'r') as file:
        vocab_words = file.readlines()

constituent_compound_mapping_dict = dict()

if args.language == 'german':
    #downloading jar for splitting the compounds
    jar_download_cmd = 'wget https://repo1.maven.org/maven2/de/danielnaber/jwordsplitter/4.4/jwordsplitter-4.4.jar'
    os.system(jar_download_cmd)

    # jwordsplitter allows max 70 characters
    vocab_words = list(filter(lambda x : len(x) < 70,vocab_words))

    with open('filtered_vocab_words','w') as file:
        for word in vocab_words:
           file.write(word+"\n")

    #running jword splitter on the vocab file
    run_splitter_cmd =  'java -jar jwordsplitter-4.4.jar filtered_vocab_words > splitted_words'
    os.system(run_splitter_cmd)

    with open('splitted_words','r') as file:
            splitted_words = file.readlines()

    for i in range(len(vocab_words)):
            if ',' in splitted_words[i]:
                    constituents = [ word.strip() for word in splitted_words[i].split(',') ]
                    for constituent in constituents:
                            compounds = constituent_compound_mapping_dict.get(constituent)
                            if compounds == None:
                                    constituent_compound_mapping_dict[constituent] = [vocab_words[i].strip()]
                            else:
                                    compounds.append(vocab_words[i].strip())


    os.system('rm -rf jwordsplitter-4.4.jar')
    os.system('rm -rf splitted_words')
    os.system('rm -rf filtered_vocab_words')

elif args.language == 'english':
    with open(ENGLISH_WORD_DICT,'r') as file:
        lines = file.readlines()

    english_word_dictionary = set()

    for line in lines:
        english_word_dictionary.add(line.strip().lower())

    for word in vocab_words:
        word = word.strip()
        constituents = get_constituents_for_compound(word,english_word_dictionary)
        if len(constituents) > 0:
            for constituent in constituents:
                compounds = constituent_compound_mapping_dict.get(constituent)
                if compounds == None:
                    constituent_compound_mapping_dict[constituent] = [word]
                else:
                    compounds.append(word)

with open(args.output_mapping_file,'w') as file:
        lines = []
        for constituent,compounds in constituent_compound_mapping_dict.items():
                        line = constituent+" "
                        line = line + " ".join(compounds)
                        lines.append(line+"\n")
        file.writelines(lines)

print("Constituent Compound Mapping file created.")

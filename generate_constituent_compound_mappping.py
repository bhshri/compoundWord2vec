import argparse
import os 
 
# Initialize parser
parser = argparse.ArgumentParser()
 
parser.add_argument("-i", "--input_vocab_file", help = "Vocab file from which constituent compound mapping will be extracted",required=True)
parser.add_argument("-o","--output_mapping_file",help = "Mapping file for constituent and compounds",required=True)
# Read arguments from command line
args = parser.parse_args()
 
#downloading jar for splitting the compounds
jar_download_cmd = 'wget https://repo1.maven.org/maven2/de/danielnaber/jwordsplitter/4.4/jwordsplitter-4.4.jar'
os.system(jar_download_cmd)

#running jword splitter on the vocab file
run_splitter_cmd =  'java -jar jwordsplitter-4.4.jar '+args.input_vocab_file+' > '+'splitted_words'
os.system(run_splitter_cmd)

with open(args.input_vocab_file,'r') as file:
        vocab_words = file.readlines()

with open('splitted_words','r') as file:
        splitted_words = file.readlines()

constituent_compound_mapping_dict = dict()

for i in range(len(vocab_words)):
        if ',' in splitted_words[i]:
                constituents = [ word.strip() for word in splitted_words[i].split(',') ]
                for constituent in constituents:
                        compounds = constituent_compound_mapping_dict.get(constituent)
                        if compounds == None:
                                constituent_compound_mapping_dict[constituent] = [vocab_words[i].strip()]
                        else:
                                compounds.append(vocab_words[i].strip())


with open(args.output_mapping_file,'w') as file:
        lines = []
        for constituent,compounds in constituent_compound_mapping_dict.items():
                        line = constituent+" "
                        line = line + " ".join(compounds)
                        lines.append(line+"\n")
        file.writelines(lines)

os.system('rm -rf jwordsplitter-4.4.jar')
os.system('rm -rf splitted_words')

print("Constituent Compound Mapping file created.")


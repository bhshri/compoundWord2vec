import argparse
import os
# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_vocab_file", help = "Vocab file from which constituent compound mapping will be extracted",required=True)
parser.add_argument("-o","--output_mapping_file",help = "Constituent compound Mapping file",required=True)
# Read arguments from command line
args = parser.parse_args()

with open(args.input_vocab_file,'r') as file:
        vocab_words = file.readlines()

constituent_compound_mapping_dict = dict()
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

with open(args.output_mapping_file,'w') as file:
        lines = []
        for constituent,compounds in constituent_compound_mapping_dict.items():
                        line = constituent+" "
                        line = line + " ".join(compounds)
                        lines.append(line+"\n")
        file.writelines(lines)

print("Constituent Compound Mapping file created.")

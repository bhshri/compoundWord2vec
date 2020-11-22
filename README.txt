SOFTWARE 
---------------------
gcc (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609
Python 3.7.1
Java (openjdk 11.0.9.1 2020-11-04)

SYSTEM CONFIGURATION
--------------------
Architecture:          x86_64
CPU(s):                8
Model name:            Intel(R) Core(TM) i7-3820 CPU @ 3.60GHz
RAM:                   32GB

PYTHON LIBRARIES
----------------
pip install pandas
pip install scikit-learn
pip install numpy
pip install scipy

DOWNLOADING AND PREPROCESSING THE TEXT CORPUS
------------------------------------------------
./download_preprocess_text_corpus.sh

Preprocessed text corpus can be downloaded from following url:
https://drive.google.com/file/d/1qIROVOOyOQqASTgwQ0cC84nc9ynHhXGy/view?usp=sharing

Smaller 500Mb corpus is obtained by applying following command on the above text corpus
head -c 500000000 text_corpus.txt > small_text_corpus.txt

GENERATING CONSTITUENT COMPOUND MAPPING FILE
--------------------------------------------
python generate_constituent_compound_mappping.py -i vocab_words -o mapping_file

vocab_words: file containing the words in German vocabulary from which compounds and their constituents will be extracted. File should contain one word per line.
mapping_file: output file created which will be used for Cword2vec training in next step.

For training Cword2vec, we use the mapping file: cword2vec_constituent_compound_mapping.txt

TRAINING Cword2vec
------------------
For Cword2vec algorithm we add 2 new arguments to default word2vec:
(1) constituent compound mapping file generated as per last step
(2) compound context augmenting probability (also called constituent_compound_replace_prob  in the word2vec.c)

Vectors can be trained by running following command.
./run_cword2vec.sh

Cword2vec vectors for which we obtained our best result is available at the following url. The vectors which are in text format have been compressed in tar.gz format:
https://drive.google.com/file/d/178e8lyVzjxg70-1iHmCm6d6bLYrPwzWe/view?usp=sharing

EVALUATING Cword2vec
--------------------
python eval.py -v Cword2vec_vectors.txt

Expected output
---------------




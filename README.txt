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

vocab_words: File containing the words from which compounds and their constituents will be extracted. File should contain one word per line.
mapping_file: Output file created which will be used for Cword2vec training in next step.

For training Cword2vec on the larger corpus, we use the mapping file: cword2vec_constituent_compound_mapping.txt
For training Cword2vec on the smaller corpus, we use the mapping file: german_small_constituent_compound_mapping_500m.txt

TRAINING Cword2vec
------------------
For Cword2vec algorithm we add 2 new arguments to default word2vec:
(1) constituent compound mapping file generated as per last step (arg name is constituent_compound_file in word2vec.c )
(2) compound context augmenting probability λ (arg name is constituent_compound_replace_prob in word2vec.c)

Vectors can be trained by running following script.
./run_cword2vec.sh

Some important arguments that can be changed in the above script are
-train:  specify the training corpus file, can be either the large corpus or small corpus file location(text_corpus.txt or small_text_corpus.txt)

-constituent_compound_file: mapping file of constituent and compounds (cword2vec_constituent_compound_mapping.txt or german_small_constituent_compound_mapping_500m.txt)

-constituent_compound_replace_prob: compound context augmenting probability λ which can take values [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

For the best results, constituent_compound_replace_prob was set 1.0 for larger corpus and 0.8 for the smaller corpus.
EVALUATING Cword2vec
--------------------
Cword2vec vectors for which we obtained our best result(both for small and large corpus) is available at the following url. 
The vectors which are in text format have been compressed in tar.gz format:
https://drive.google.com/file/d/1OjkENisdKygRMNe2C2f_GWKlxW0PsfZK/view?usp=sharing

Expected output for the vector file(Cword2vec_large.txt) trained on larger corpus shared on the google drive.
------------------------------------------------------------------------------------------------------------
python eval.py -v Cword2vec_large.txt -s large

Spearman correlation
0.3033887349462969
Kendall correlation
0.20290645238491906
RMSE
0.2816375933741194

Expected output for the vector file(Cword2vec_small.txt) trained on smaller corpus shared on the google drive.
-------------------------------------------------------------------------------------------------------------
python eval.py -v Cword2vec_small.txt -s small

Spearman correlation
0.3518891375583033
Kendall correlation
0.2553930675525646
RMSE
0.2623627861379514

**Note: Both the results above are the best results obtained on the large and small corpus.

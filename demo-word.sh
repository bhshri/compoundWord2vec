make
time ./word2vec -train 'text_corpus.txt' -output vectors.txt -cbow 0 -window 10 -negative 5 -threads 8 -binary 0 -iter 5 -save-vocab vocab.txt -constituent_compound_file 'constituent_compound_filtered.txt' 

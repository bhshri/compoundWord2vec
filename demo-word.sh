make
time ./word2vec -train 'text_corpus.txt' -output Cword2vec_vectors.txt -cbow 0 -window 10 -negative 5 -threads 16 -binary 0 -iter 5 -save-vocab vocab.txt -constituent_compound_file 'cword2vec_constituent_compound_mapping.txt' -constituent_compound_replace_prob 1.0

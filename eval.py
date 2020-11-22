import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math
from scipy.stats import spearmanr
from scipy.stats.stats import kendalltau
from sklearn.metrics import mean_squared_error
import argparse


def get_vectors_from_txt_file(filepath):
    model = dict()
    with open(filepath) as f:
        for line in f:
            word, *vector = line.split()
            model[word] = np.array(vector, dtype=np.float32)[:100]
    return model



# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--vec_file", help = "word vector file in text format",required=True)
parser.add_argument("-s", "--size", help = "large or small, indicates the corpus size used ",required=True)
# Read arguments from command line
args = parser.parse_args()

compound_words_dataframe = pd.read_csv('DATASETS/compound_word_pair_dataframe.csv')
model = get_vectors_from_txt_file(args.vec_file)
vocab = model.keys()

compound_ref_similarity_values    =  [] 
compound_cosine_similarity_values =  []


for i in range(compound_words_dataframe.shape[0]):
        word_1 = compound_words_dataframe['WORD1'][i].lower()
        word_2 = compound_words_dataframe['WORD2'][i].lower() 
        word_1_vector = np.zeros((100,)).reshape(1,-1)
        word_2_vector = np.zeros((100,)).reshape(1,-1)
        
        if word_1 in vocab:
            word_1_vector = model.get(word_1).reshape(1,-1)
        elif args.size == 'small':
            continue
        if word_2 in vocab:
            word_2_vector = model.get(word_2).reshape(1,-1)
        elif args.size == 'small':
            continue
        
        value = cosine_similarity(word_1_vector,word_2_vector)[0][0]
        compound_cosine_similarity_values.append(value)
        compound_ref_similarity_values.append(compound_words_dataframe['GROUND_TRUTH_SIMILARITY'][i]/4)

        

coef, p = spearmanr(compound_ref_similarity_values, compound_cosine_similarity_values)

print('Spearman correlation')
print(coef)


tau,p = kendalltau(compound_ref_similarity_values, compound_cosine_similarity_values)

print('Kendall correlation')
print(tau)


RMSE = math.sqrt(mean_squared_error(compound_ref_similarity_values, compound_cosine_similarity_values))

print('RMSE')
print(RMSE)
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math
from scipy.stats import spearmanr
from scipy.stats.stats import kendalltau
from sklearn.metrics import mean_squared_error
import argparse


def get_vectors_from_txt_file(filepath):
    model = dict()
    with open(filepath) as f:
        for line in f:
            word, *vector = line.split()
            model[word] = np.array(vector, dtype=np.float32)[:100]
    return model



# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--vec_file", help = "word vector file in text format",required=True)
parser.add_argument("-s", "--size", help = "large or small, indicates the corpus size used ",required=True)
# Read arguments from command line
args = parser.parse_args()

compound_words_dataframe = pd.read_csv('DATASETS/compound_word_pair_dataframe.csv')
model = get_vectors_from_txt_file(args.vec_file)
vocab = model.keys()

compound_ref_similarity_values    =  [] 
compound_cosine_similarity_values =  []


for i in range(compound_words_dataframe.shape[0]):
        word_1 = compound_words_dataframe['WORD1'][i].lower()
        word_2 = compound_words_dataframe['WORD2'][i].lower() 
        word_1_vector = np.zeros((100,)).reshape(1,-1)
        word_2_vector = np.zeros((100,)).reshape(1,-1)
        
        if word_1 in vocab:
            word_1_vector = model.get(word_1).reshape(1,-1)
        elif args.size == 'small':
            continue
        if word_2 in vocab:
            word_2_vector = model.get(word_2).reshape(1,-1)
        elif args.size == 'small':
            continue
        
        value = cosine_similarity(word_1_vector,word_2_vector)[0][0]
        compound_cosine_similarity_values.append(value)
        compound_ref_similarity_values.append(compound_words_dataframe['GROUND_TRUTH_SIMILARITY'][i]/4)

        

coef, p = spearmanr(compound_ref_similarity_values, compound_cosine_similarity_values)

print('Spearman correlation')
print(coef)


tau,p = kendalltau(compound_ref_similarity_values, compound_cosine_similarity_values)

print('Kendall correlation')
print(tau)


RMSE = math.sqrt(mean_squared_error(compound_ref_similarity_values, compound_cosine_similarity_values))

print('RMSE')
print(RMSE)

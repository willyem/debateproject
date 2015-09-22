import processing
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import linear_kernel
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np


for_, aga_=  processing.parse_text('immigrants.txt')

docs = [word_tokenize(for_)]
#vectorizer = TfidfVectorizer(stop_words='english')
#vectors = vectorizer.fit_transform(data).toarray()
#words = vectorizer.get_feature_names() 

print docs
import processing
import string 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
import numpy as np

list_of_document_names = ['guns.txt', 'immigrants.txt'] 
wordnet = WordNetLemmatizer()
stop = set(stopwords.words('english'))
all_words = [] 

for document in list_of_document_names: 

    for_, aga_=  processing.parse_text(document) #/document

    ##tokenize 'for_'
    tokenized_for = word_tokenize(for_[0].decode('unicode_escape').encode('ascii', 'ignore'))
    tokenized_aga = word_tokenize(aga_[0].decode('unicode_escape').encode('ascii', 'ignore'))

    for_wo_punctuation_words = [x for x in tokenized_for if x not in string.punctuation]
    aga_wo_punctuation_words = [x for x in tokenized_aga if x not in string.punctuation]

    docs_for = [word for word in for_wo_punctuation_words if word not in stop] 
    docs_aga = [word for word in aga_wo_punctuation_words if word not in stop] 

    all_words += for_ + aga_

#docs_wordnet = [wordnet.lemmatize(word) for word in all_words]

#docs = docs_wordnet

#vocab_set = set()

#[vocab_set.add(token) for token in docs]

#vocab = list(vocab_set)

#cv = CountVectorizer(stop_words = 'english')
#vectorized = cv.fit_transform(for_+aga_)
def tokenize(doc):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    '''
    return [wordnet.lemmatize(word) for word in word_tokenize(doc.lower())]

tfidf = TfidfVectorizer(stop_words='english')
tfidfed = tfidf.fit_transform(all_words).toarray()

#print tfidfed

cosine_similarities = linear_kernel(tfidfed, tfidfed)

print cosine_similarities

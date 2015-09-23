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

wordnet = WordNetLemmatizer()
for_, aga_=  processing.parse_text('guns.txt')

##tokenize 'for_'
tokenized_for = word_tokenize(for_[0].decode('unicode_escape').encode('ascii', 'ignore'))
tokenized_aga = word_tokenize(aga_[0].decode('unicode_escape').encode('ascii', 'ignore'))

for_wo_punctuation_words = [x for x in tokenized_for if x not in string.punctuation]
aga_wo_punctuation_words = [x for x in tokenized_aga if x not in string.punctuation]

stop = set(stopwords.words('english'))

docs_for = [word for word in for_wo_punctuation_words if word not in stop] 
docs_aga = [word for word in aga_wo_punctuation_words if word not in stop] 

all_words = docs_for + docs_aga

docs_wordnet = [wordnet.lemmatize(word) for word in all_words]

docs = docs_wordnet

vocab_set = set()

[vocab_set.add(token) for token in docs]

vocab = list(vocab_set)

cv = CountVectorizer(stop_words = 'english')
vectorized = cv.fit_transform(for_+aga_)

tfidf = TfidfVectorizer(stop_words='english')
tfidfed = tfidf.fit_transform(for_+aga_).toarray()

#print tfidfed

cosine_similarities = linear_kernel(tfidfed[0], tfidfed)

print cosine_similarities

#pos_tagged = [pos_tag(docs_wordnet)]

#print pos_tagged
#print docs_wordnet

#content = for_[0].encode('ascii', 'ignore')
#content = for_[0].decode('utf-8')
#print content.lower()
#print word_tokenize(content.lower())
#vectorizer = TfidfVectorizer(stop_words='english')
#vectors = vectorizer.fit_transform(data).toarray()
#words = vectorizer.get_feature_names() 
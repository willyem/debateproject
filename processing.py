import re
import processing
import pandas as pd
import string 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
import numpy as np
from textblob import TextBlob
from textstat.textstat import textstat 

wordnet = WordNetLemmatizer()
stop = set(stopwords.words('english'))


'''
def tokenize(text): 

    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    
    return [wordnet.lemmatize(word) for word in word_tokenize(doc.lower())]
'''
def parse_text(filename): 
#Opens up a txt file and splits on new lines; 
#removes empty items from list 

	temp_file = open(filename)
	temp_text = temp_file.read()
#	temp_text = temp_text.replace("\'", "")
	working_text = temp_text.split('\n')

	working_text = [x.strip() for x in working_text if (x != " ") and (x != "")]


	working_text = clean_text(working_text)

	for_speakers, against_speakers, moderator = get_speakers(working_text)

	non_for = against_speakers + moderator
	non_aga = for_speakers + moderator

	for_motion_text = get_motion_text(for_speakers, non_for, working_text)
	aga_motion_text = get_motion_text(against_speakers, non_aga, working_text)

	for_motion_text = decode_text(for_motion_text)
	aga_motion_text = decode_text(aga_motion_text)

	lc_for = get_laughter_count(for_motion_text)
	ac_for = get_applause_count(for_motion_text)
	
	lc_aga = get_laughter_count(aga_motion_text)
	ac_aga = get_applause_count(aga_motion_text)

	#makes 'for_motion_text' into a single string
	for_motion_text = [' '.join([' '.join(item) for item in for_motion_text])]

	#makes 'aga_motion_text' into a single string
	aga_motion_text = [' '.join([' '.join(item) for item in aga_motion_text])]


	for_sc, for_ari, for_flesch = get_textstats(for_motion_text[0])
	aga_sc, aga_ari, aga_flesch = get_textstats(aga_motion_text[0])

	for_pol, for_subj = get_sentiment_analysis(for_motion_text[0])
	aga_pol, aga_subj = get_sentiment_analysis(aga_motion_text[0])
	
	#Returns text, laughter, applause, polarity, and subjectivity for 
	#both for and against motion text

	return for_motion_text, lc_for, ac_for, for_pol, for_subj, for_sc, for_ari, for_flesch, \
			aga_motion_text, lc_aga, ac_aga, aga_pol, aga_subj, aga_sc, aga_ari, aga_flesch
			
#	return for_speakers, against_speakers

#	print filename
#	print for_speakers
#	for speaker in for_motion_text: 
#		print speaker
#	print against_speakers
#	for speaker in aga_motion_text:
#		print len(speaker)
#	print '\n\n\n'

#	print for_motion_text
#	print for_speakers, against_speakers
#	for something in for_motion_text: 
#		for sentence in something: 
#			print sentence
#			print TextBlob(sentence).sentiment


''' counts the number of times laughter is in the text'''

def get_textstats(text): 
	return textstat.sentence_count(text), textstat.automated_readability_index(text), textstat.flesch_reading_ease(text)

def get_sentiment_analysis(text): 
	temp = TextBlob(text)
	return temp.sentiment.polarity, temp.sentiment.subjectivity


def get_laughter_count(text):
	return sum([sum([sentence.count('[laughter]') + sentence.count('LAUGHTER') \
			for sentence in speaker]) for speaker in text])


''' counts the number of times the audience applauses in the text''' 

def get_applause_count(text):
	return sum([sum([sentence.count('[applause]') + sentence.count('APPLAUSE') \
			for sentence in speaker]) for speaker in text])


''' decodes the text from unicode and encodes it as ascii ''' 

def decode_text(text): 
	return [[item.decode('unicode_escape').encode('ascii', 'ignore') \
						for item in entry] for entry in text]


''' determines the speakers for the motion and against the motion in the text ''' 

def get_speakers(working_text): 

	for_motion = []
	against_motion = []
	moderator = []
	for line in working_text:
	    if line.lower().startswith("for the motion:") and ('%' not in line):
	        line = line.replace(" and ", ":")
	        line = line.replace(" & ", ":")
	        line = line.replace(",",":")
	        for item in line.split(":")[1:]:
	            for_motion.append(item.strip()+":")
	        
	    elif line.lower().startswith("against the motion:") and ('%' not in line): 
	        line = line.replace(" and ", ":")
	        line = line.replace(",",":")
	        for item in line.split(":")[1:]:
	            against_motion.append(item.strip()+":")
	            
	    elif line.lower().startswith("moderator:"): 
	        moderator.append(line.split(":")[1].strip()+":")

	for_motion = [item.decode('unicode_escape').encode('ascii', 'ignore') for item in for_motion]
	against_motion = [item.decode('unicode_escape').encode('ascii', 'ignore') for item in against_motion]

	return for_motion, against_motion, moderator 

''' creates a list where each item is a time where a given speaker said something ''' 

def get_motion_text(motion_speakers, non_motion_speakers, working_text):


	#Puts all "for the motion" text into a list 

	motion_speakers_text = []
	started = False

	for speaker in motion_speakers:

	    other_motion_speakers = [person for person in motion_speakers if person != speaker]

	    speaker_text = [] 

	    for index, line in enumerate(working_text):
	        if ((speaker in line) or (speaker.upper()[:-1] in line)) and (started==False): 
	            start_index = index
	            started = True


	        elif started == True: 
	            for non_speaker in non_motion_speakers + other_motion_speakers:

	                if (non_speaker in line) or (non_speaker.upper()[:-1] in line): 
	                    speaker_text.append(working_text[start_index+1:index])
	                    started = False

	    motion_speakers_text.append([' '.join(item) for item in speaker_text])

	return motion_speakers_text

''' cleans up the text by removing headers/footers; not the neatest, but it works''' 

def clean_text(working_text):

	numbers = re.compile('\d{4}$')
	timestamp = re.compile('\d{2}:\d{2}:\d{2}$')
	pagenumber = re.compile('Page..?\d{1}.?$')
	date = re.compile('.?\d{1}/.?\d{1}/.?.?\d{2}$')
	anotherpagenumber = re.compile('Intelligence Squared U.S. -.?.?.?.?.?-.?.?.?.?$')
	
	return [line for line in working_text if \
					(numbers.search(line) == None) and \
					(timestamp.search(line) == None) and \
					(pagenumber.search(line) == None) and \
					(date.search(line) == None) and \
					(anotherpagenumber.search(line) == None) and \
					("Media Transcripts, Inc." not in line) and \
					("-Intelligence Square U.S.-" not in line) and \
					("-Intelligence Squared U.S.-" not in line) and \
					("\"Intelligence Squared U.S.\"" not in line) and \
					("\"Intelligence Square U.S.\"" not in line) and \
					("PROGRAM" not in line)]
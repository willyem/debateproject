import re
from textblob import TextBlob 

def parse_text(filename): 
#Opens up a txt file and splits on new lines; 
#removes empty items from list 
#creates empty lists for the speakers 

	temp_file = open(filename)
	temp_text = temp_file.read()
	working_text = temp_text.split('\n')
	working_text = [x.strip() for x in working_text if (x != " ") and (x != "")]

	#removes lines where the last 4 characters are numbers (address line
	#telephone line); POSSIBLE that it might remove a line where someone is 
	#talking, but I don't foresee that being a huge problem. 
	#also removes lines
	#where the first characters are XX:XX:XX (timestamp lines)

	numbers = re.compile('\d{4}$')
	timestamp = re.compile('\d{2}:\d{2}:\d{2}$')
	pagenumber = re.compile('Page..?\d{1}.?$')

	#relists the lines so that they don't contain those 'bad' lines
	
	working_text = [line for line in working_text if \
					(numbers.search(line) == None) and \
					(timestamp.search(line) == None) and \
					(pagenumber.search(line) == None) and \
					("Media Transcripts, Inc." not in line) and \
					("-Intelligence Square U.S.-" not in line)]

#	for line in working_text: 
#		print line

	for_speakers, against_speakers, moderator_speaker = get_speakers(working_text)

	non_for = against_speakers + moderator_speaker
	non_aga = for_speakers + moderator_speaker

	for_motion_text = get_motion_text(for_speakers, non_for, working_text)
	aga_motion_text = get_motion_text(against_speakers, non_aga, working_text)

	#for_motion_text contains an item for each speaker; 
	#each item is a list of sentences that that speaker said. 

	for_motion_text = decode_text(for_motion_text)
	aga_motion_text = decode_text(aga_motion_text)

	print filename
	print for_speakers
	print against_speakers
	print '\n\n\n'

#	print for_motion_text
#	print for_speakers, against_speakers
#	for something in for_motion_text: 
#		for sentence in something: 
#			print sentence
#			print TextBlob(sentence).sentiment


def decode_text(text): 
	return [[item.decode('unicode_escape').encode('ascii', 'ignore') \
						for item in entry] for entry in text]

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


def get_motion_text(motion_speakers, non_motion_speakers, working_text):


	#Puts all "for the motion" text into a list 

	motion_speakers_text = []
	started = False

	for speaker in motion_speakers:

	    speaker_text = [] 

	    for index, line in enumerate(working_text):
	        if ((speaker in line) or (speaker.upper()[:-1] in line)) and (started==False): 
	            start_index = index
	            started = True


	        elif started == True: 
	            for anti in non_motion_speakers:

	                if (anti in line) or (anti.upper()[:-1] in line): 
	                    speaker_text.append(working_text[start_index+1:index])
	                    started = False

	    motion_speakers_text.append([' '.join(item) for item in speaker_text])

	return motion_speakers_text
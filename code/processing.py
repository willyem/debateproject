
def parse_text(filename): 
#Opens up a txt file and splits on new lines; 
#removes empty items from list 
#creates empty lists for the speakers 

	temp_file = open(filename)
	temp_text = temp_file.read()
	working_text = temp_text.split('\n')
	working_text = [x.strip() for x in working_text if (x != " ") and (x != "")]
	for_motion = []
	against_motion = []
	moderator = []

	#finds the line with the "for the motion" speakers and appends 
	#speaker names + ":"


	for line in working_text:
	    if line.lower().startswith("for the motion:"):
	        line = line.replace(" and ", ":")
	        line = line.replace(",",":")
	        for item in line.split(":")[1:]:
	            for_motion.append(item.strip()+":")
	        
	for line in working_text: 
	    if line.lower().startswith("against the motion:"): 
	        line = line.replace(" and ", ":")
	        line = line.replace(",",":")
	        for item in line.split(":")[1:]:
	            against_motion.append(item.strip()+":")
	            
	for line in working_text: 
	    if line.lower().startswith("Moderator"):
#	    	print line 
	        moderator.append(line.split(":")[1].strip()+":")

	#Puts all "for the motion" text into a list 

	for_the_motion_text = []
	started = False
	against_and_moderator = against_motion+moderator

	for speaker in for_motion:

	    for index, line in enumerate(working_text):
	    
#	    	print index, line
	        if ((speaker in line) or (speaker.upper()[:-1] in line)) and (started==False): 
	            start_index = index
	            started = True


	        if started == True: 
	            for anti in against_and_moderator: 
	                if (anti in line) or (anti.upper()[:-1] in line): 
	                    for_the_motion_text.append(working_text[start_index+1:index])
	                    started = False

	#puts all the against the motion text into a list 

	against_the_motion_text = []
	started = False
	for_and_moderator = for_motion+moderator

	for speaker in against_motion:


	    for index, line in enumerate(working_text):
	    	
	        #if the current speaker is in the line (some documents have the speakers listed as 
	        #	SPEAKER NAME [all caps] so the second part of 'or' accounts for that) and (started==False): 
	        if ((speaker in line) or (speaker.upper()[:-1] in line)) and (started == False): 
	            start_index = index
	            started = True
	                
	        if started == True: 
	            for pro in for_and_moderator: 
	                if (pro in line) or (pro.upper()[:-1] in line): 
	                    against_the_motion_text.append(working_text[start_index+1:index])
	                    started = False
	
	all_for_text = [' '.join([' '.join(item) for item in for_the_motion_text])]
	all_against_text = [' '.join([' '.join(item) for item in against_the_motion_text])]
	#returns the for the motion text and the against the motion text
	return all_for_text, all_against_text
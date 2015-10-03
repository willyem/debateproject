import processing
import pandas as pd
import string 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk.data
from nltk.corpus import stopwords
from nltk import pos_tag
import numpy as np

#[0] = name of document 
#[1] = winner of debate; [x, y] --> x = For, y = Against
#[2] = gender of speaker; 0 = male, 1 = female 

'''
names_and_win = [('campus_assault.txt', [0, 1], [(0, 1), (1, 0)]), ('samesex.txt', [0, 1], [(0, 0), (0, 0)]), ('iran_deal.txt', [0, 1], [(0, 0), (0, 0)]),\
('death_penalty.txt', [0, 1], [(1, 0), (0, 0)]), ('constitutional_authority.txt', [0, 1], [(0, 1), (0, 0)]), ('right_to_forget.txt', [0, 1], [(0, 0), (0, 0)]), \
('liberals_stifling.txt', [1, 0], [(0, 1), (0, 0)]), ('declinists.txt', [1, 0], [(0, 0), (1, 0)]), ('amazon.txt', [0, 1], [(0, 0), (0, 0)]), ('gmos.txt', [1, 0], [(0, 1), (0, 1)]), \
('eutha.txt', [0, 1], [(0, 0), (1, 0)]), \
('income_inequal.txt', [0, 1], [(1, 0), (0, 0)]), ('mass_collection.txt', [1, 0], [(0, 1), (0, 0)]), ('flexing_musc.txt', [1, 0], [(0, 0), (0, 0)]), ('common_core.txt', [1, 0], [(1, 0), (1, 0)]), \
('pacs.txt', [0, 1], [(0, 1), (0, 1)]), ('death_not_final.txt', [0, 1], [(0, 0), (0, 0)]), ('millenials.txt', [1, 0], [(1, 0), (0, 1)]), ('lecture_obsolete.txt', [1, 0], [(0, 0), (0, 1)]), \
('russia.txt', [0, 1], [(0, 0), (0, 0)]), ('USA_kill.txt', [1, 0], [(0, 0), (0, 1)]), ('affirmative.txt', [1, 0], [(1, 0), (0, 0)]), ('snowden.txt', [1, 0], [(0, 0), (0, 0)]), ('obamacare.txt', [1, 0], [(0, 1), (0, 0)]), \
('eat_face.txt', [1, 0], [(0, 0), (0, 0)]), ('spy_on_me.txt', [0, 1], [(0, 0), (0, 0)]), ('right_to_bear.txt', [1, 0], [(0, 0), (0, 0)]), ('take_job_anywhere.txt', [0, 1], [(0, 0), (1, 0)]), \
('red_state.txt', [1, 0], [(0, 0), (0, 0)]), ('break_up_banks.txt', [0, 1], [(0, 0), (0, 0)]), ('drones.txt', [0, 1], [(0, 0), (0, 0)]), ('us_syria.txt', [1, 0], [(0, 0), (0, 0)]), \
('pentagon_budget.txt', [0, 1], [(0, 0), (0, 1)]), ('fda_caution.txt', [1, 0], [(0, 0), (0, 0)]), ('gop_center.txt', [0, 1], [(0, 0), (1, 0)]), ('minimum_wage.txt', [0, 1], [(0, 0), (0, 1)]), \
('strong_dollar.txt', [1, 0], [(0, 0), (0, 0)]), ('prohibit_genetic.txt', [0, 1], [(0, 0), (1, 0)]), ('nuclear_iran.txt', [0, 1], [(0, 0), (0, 0)]), ('science_god.txt', [1, 0], [(0, 0), (0, 0)]), \
('legalize_drugs.txt', [1, 0], [(0, 0), (0, 0)]), ('rich_taxed.txt', [0, 1], [(0, 0), (0, 0)]), ('end_of_life_care.txt', [1, 0], [(0, 0), (0, 1)]), ('elected_islamists.txt', [0, 1], [(0, 0), (0, 0)]),\
('money_politics_overregulated.txt', [0, 1], [(0, 0), (0, 0)]), ('natural_gas_bad.txt', [1, 0], [(1, 1), (0, 1)]), ('ban_football.txt', [1, 0], [(0, 0), (0, 0)]), \
('internet_closing_minds.txt', [1, 0], [(0, 0), (0, 0)]), ('china_capitalism_better.txt', [0, 1], [(0, 0), (0, 0)]), ('obesity_govt_business.txt', [0, 1], [(1, 0), (0, 0)]), \
('palestine_statehood.txt', [1, 0], [(0, 0), (0, 0)]), ('no_religion.txt', [1, 0], [(0, 0), (0, 0)]), ('job_plan.txt', [1, 0], [(1, 0), (0, 0)]), ('too_many_kids_college.txt', [1, 0], [(0, 0), (0, 0)]), \
('grandmas_benefits.txt', [0, 1], [(1, 0), (0, 0)]), ('men_are_finished.txt', [1, 0], [(0, 1), (1, 0)]), ('end_war_on_terror.txt', [0, 1], [(0, 1), (0, 0)]), \
('freedom_press_state.txt', [0, 1], [(0, 0), (0, 0)]), ('dont_give_us.txt', [1, 0], [(0, 0), (1, 0)]), ('clip_americas_wings.txt', [1, 0], [(0, 0), (0, 0)]), \
('clean_energy.txt', [0, 1], [(0, 1), (0, 0)]), ('two_party_bad.txt', [0, 1], [(0, 1), (0, 0)]), ('repeal_obamacare.txt', [0, 1], [(0, 0), (0, 0)]), ('airports_profiling.txt', [1, 0], [(0, 0, 1), (0, 1, 0)]), \
('afghanistan_lost.txt', [0, 1], [(0, 0), (0, 0)]), ('big_govt_stifling.txt', [1, 0], [(0, 0), (0, 1)]), ('islam_is_peace.txt', [0, 1], [(1, 0), (1, 0)]), \
('terrorists_enemy_combatants.txt', [0, 1], [(0, 0), (0, 0)]), ('cyber_war_exaggerated.txt', [0, 1], [(0, 0), (0, 0)]), ('obamas_policy_us_decline.txt', [0, 1], [(0, 0), (0, 0)]), \
('organic_is_hype.txt', [0, 1], [(0, 0, 0), (0, 1, 0)]), ('teacher_unions_failing_schools.txt', [0, 1], [(1, 0, 1), (0, 0, 0)]), ('us_stepback_israel.txt', [1, 0], [(0, 0), (0, 0)]), \
('california_failed.txt', [1, 0], [(0, 0, 1), (0, 0, 0)]), ('us_mexico_drugs.txt', [1, 0], [(0, 0, 0), (0, 0, 0)]), ('obamas_policies_working.txt', [1, 0], [(0, 0, 0), (0, 0, 0)]), \
('good_riddance_mainstream.txt', [0, 1], [(0, 0, 0), (0, 0, 1)]), ('us_will_not_succeed_afghan.txt', [0, 1], [(0, 0, 0), (0, 0, 0)]), ('buy_american_bad.txt', [1, 0], [(0, 0, 1), (0, 0, 0)]), \
('diplomacy_iran_nowhere.txt', [0, 1], [(1, 0), (0, 0)]), ('pay_for_sex.txt', [1, 0], [(1, 1, 1), (1, 0, 0)]), ('blame_washington_financial.txt', [1, 0], [(0, 0, 0), (0, 0, 1)]), \
('art_market_ethical.txt', [1, 0], [(0, 0, 0), (1, 0, 0)]), ('carbon_reductions_not_worth_it.txt', [1, 0], [(0, 0, 0), (1, 0, 0)]), ('bush_is_worst.txt', [0, 1], [(0, 0), (0, 0)]), \
('google_dont_be_evil.txt', [1, 0], [(0, 0, 0), (1, 0, 0)]), ('guns_reduce_crime.txt', [1, 0], [(0, 0, 0), (0, 0, 0)]), ('america_winning_iraq.txt', [1, 0], [(0, 0), (0, 0)]), \
('universal_health.txt', [0, 1], [(0, 0, 0), (0, 1, 0)]), ('legalize_organs.txt', [1, 0], [(0, 1, 1), (0, 0, 0)]), ('islam_radicals.txt', [1, 0], [(0, 0, 1), (0, 0, 1)]), \
('tough_interrogation.txt', [0, 1], [(0, 1, 0), (0, 0, 0)]), ('america_policeman.txt', [1, 0], [(0, 0, 0), (0, 1, 0)]), ('performance_enhancing.txt', [1, 0], [(0, 0, 0), (0, 0, 0)]), \
('aid_africa_bad.txt', [0, 1], [(0, 0, 0), (0, 0, 1)]), ('end_affirmative.txt', [0, 1], [(0, 0, 0), (1, 1, 0)]), ('russia_enemy_again.txt', [0, 1], [(1, 0, 0), (1, 0, 0)]), \
('stop_welcoming_immigrants.txt', [1, 0], [(0, 0, 1), (0, 0, 1)]), ('spread_democracy_me.txt', [1, 0], [(0, 0, 0), (1, 1, 0)]), ('booming_china.txt', [0, 1], [(0, 0, 0), (0, 0, 0)]), \
('more_domestic_surveillance.txt', [0, 1], [(0, 0, 0), (0, 0, 1)]), ('global_warming_not.txt', [1, 0], [(0, 0, 0), (1, 0, 0)]), ('america_too_religious.txt', [1, 0], [(1, 0, 0), (1, 0, 0)]), \
('hollywood_anti_us.txt', [0, 1], [(0, 0, 0), (1, 0, 0)]), ('democratic_hamas.txt', [0, 1], [(0, 0, 0), (0, 0, 0)]), ('license_to_offend.txt', [1, 0], [(0, 0, 1), (0, 1, 1)]), \
('tolerate_iran.txt', [1, 0], [(0, 0, 0), (0, 0, 0)])]
'''

names_and_win2 = [('campus_assault.txt', [0, 1])]
stop = set(stopwords.words('english'))

all_words = [] 

df = pd.DataFrame(columns = ["For_text", "FL", "FA", "FP", "FS", \
                             "Against_text", "AL", "AA", "AP", "AS"])


#inserts values from parse_text into dataframe at the given position
i = 0
for document in names_and_win:
    
    df.loc[i] =  processing.parse_text('debate_text/'+document[0]) #/document
    i += 1 



#creates a list of items where each item refers to either a for the motion text (0-106) 
#or against the motion text (107-214); 

all_text = []
for row in df['For_text']:
    all_text.append(row)

for row in df['Against_text']: 
    all_text.append(row)

all_text = [' '.join(item) for item in all_text]

# tfidf-erizes each for the motion and against the motion text \\ 
# appends the DIFFERENCE between the two to a new column 
# known as vector differences
tfidf = TfidfVectorizer(stop_words = 'english')
tfidf_vectors = tfidf.fit_transform(all_text)

vector_differences = tfidf_vectors[0:107] - tfidf_vectors[107:214]

df['Vector_differences'] = list(vector_differences.todense())


#generates list of who won/lost the debate and sets it as a feature in df

for_the_motion_win_classification = []
for item in names_and_win: 
    for_the_motion_win_classification.append(item[1][0])

#who_won --> 0 means against the motion won, 1 means for the motion won

df['who_won'] = for_the_motion_win_classification




#finds the avg of each vector_difference for all of the debates in which 
#for the motion won, and all of the debates in which against the motion won 
#then goes through and calculates a given debates cosine similarity to these 
#two averages and appends those values to the DataFrame

#in theory, the higher a debates similarity to a given 'avg', the more likely 
#it is that that side won the debate 

sum_of_aga_motion_tfidf_winners = sum(df[df['who_won']==0]['Vector_differences'])
aga_wins_avg_tfidf = sum_of_aga_motion_tfidf_winners/len(df[df['who_won']==0])

sum_of_for_motion_tfidf_winners = sum(df[df['who_won']==1]['Vector_differences'])
for_wins_avg_tfidf = sum_of_for_motion_tfidf_winners/len(df[df['who_won']==1])

cosim_to_aga_wins_avg_tfidf = linear_kernel(aga_wins_avg_tfidf, vector_differences)
cosim_to_for_wins_avg_tfidf = linear_kernel(for_wins_avg_tfidf, vector_differences)

df['cosim_to_for_wins'] = cosim_to_for_wins_avg_tfidf.reshape(107, 1)
df['cosim_to_aga_wins'] = cosim_to_aga_wins_avg_tfidf.reshape(107, 1)
























'''
    print for_
    print '\n\n\n\n\n\n\n\n\n\n'
    print aga_
    print '\n\n\n\n\n\n\n\n\n\n'
    ##tokenize 'for_'
    tokenized_for = word_tokenize(for_[0].decode('unicode_escape').encode('ascii', 'ignore'))
    tokenized_aga = word_tokenize(aga_[0].decode('unicode_escape').encode('ascii', 'ignore'))

    for_wo_punctuation_words = [x for x in tokenized_for if x not in string.punctuation]
    aga_wo_punctuation_words = [x for x in tokenized_aga if x not in string.punctuation]

    docs_for = [word for word in for_wo_punctuation_words if word not in stop] 
    docs_aga = [word for word in aga_wo_punctuation_words if word not in stop] 

    all_words += for_ + aga_


tfidf = TfidfVectorizer(stop_words='english')
tfidfed = tfidf.fit_transform(all_words).toarray()

#print tfidfed

cosine_similarities = linear_kernel(tfidfed, tfidfed)

#df = pd.DataFrame(tfidfed)

#print cosine_similarities
#for index, vector in enumerate(tfidfed): 
#    if sum(vector) == 0.0:
#        print index 
'''
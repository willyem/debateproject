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


names_and_win = [('campus_assault.txt', [0, 1]), ('ISIS_defeated.txt', [0, 1]), ('samesex.txt', [0, 1]), ('iran_deal.txt', [0, 1]),\
('death_penalty.txt', [0, 1]), ('constitutional_authority.txt', [0, 1]), ('right_to_forget.txt', [0, 1]), \
('liberals_stifling.txt', [1, 0]), ('declinists.txt', [1, 0]), ('amazon.txt', [0, 1]), ('gmos.txt', [1, 0]), ('eutha.txt', [0, 1]), \
('income_inequal.txt', [0, 1]), ('mass_collection.txt', [1, 0]), ('flexing_musc.txt', [1, 0]), ('common_core.txt', [1, 0]), \
('pacs.txt', [0, 1]), ('death_not_final.txt', [0, 1]), ('millenials.txt', [1, 0]), ('lecture_obsolete.txt', [1, 0]), \
('russia.txt', [0, 1]), ('USA_kill.txt', [1, 0]), ('affirmative.txt', [1, 0]), ('snowden.txt', [1, 0]), ('obamacare.txt', [1, 0]), \
('eat_face.txt', [1, 0]), ('spy_on_me.txt', [0, 1]), ('right_to_bear.txt', [1, 0]), ('take_job_anywhere.txt', [0, 1]), \
('red_state.txt', [1, 0]), ('break_up_banks.txt', [0, 1]), ('drones.txt', [0, 1]), ('us_syria.txt', [1, 0]), \
('pentagon_budget.txt', [0, 1]), ('fda_caution.txt', [1, 0]), ('gop_center.txt', [0, 1]), ('minimum_wage.txt', [0, 1]), \
('strong_dollar.txt', [1, 0]), ('prohibit_genetic.txt', [0, 1]), ('nuclear_iran.txt', [0, 1]), ('science_god.txt', [1, 0]), \
('legalize_drugs.txt', [1, 0]), ('rich_taxed.txt', [0, 1]), ('end_of_life_care.txt', [1, 0]), ('elected_islamists.txt', [0, 1]),\
('money_politics_overregulated.txt', [0, 1]), ('natural_gas_bad.txt', [1, 0]), ('ban_football.txt', [1, 0]), \
('internet_closing_minds.txt', [1, 0]), ('china_capitalism_better.txt', [0, 1]), ('obesity_govt_business.txt', [0, 1]), \
('palestine_statehood.txt', [1, 0]), ('no_religion.txt', [1, 0]), ('job_plan.txt', [1, 0]), ('too_many_kids_college.txt', [1, 0]), \
('grandmas_benefits.txt', [0, 1]), ('men_are_finished.txt', [1, 0]), ('end_war_on_terror.txt', [0, 1]), \
('freedom_press_state.txt', [0, 1]), ('dont_give_us.txt', [1, 0]), ('clip_americas_wings.txt', [1, 0]), \
('clean_energy.txt', [0, 1]), ('two_party_bad.txt', [0, 1]), ('repeal_obamacare.txt', [0, 1]), ('airports_profiling.txt', [1, 0]), \
('afghanistan_lost.txt', [0, 1]), ('big_govt_stifling.txt', [1, 0]), ('islam_is_peace.txt', [0, 1]), \
('terrorists_enemy_combatants.txt', [0, 1]), ('cyber_war_exaggerated.txt', [0, 1]), ('obamas_policy_us_decline.txt', [0, 1]), \
('organic_is_hype.txt', [0, 1]), ('teacher_unions_failing_schools.txt', [0, 1]), ('us_stepback_israel.txt', [1, 0]), \
('california_failed.txt', [1, 0]), ('us_mexico_drugs.txt', [1, 0]), ('obamas_policies_working.txt', [1, 0]), \
('good_riddance_mainstream.txt', [0, 1]), ('us_will_not_succeed_afghan.txt', [0, 1]), ('buy_american_bad.txt', [1, 0]), \
('diplomacy_iran_nowhere.txt', [0, 1]), ('pay_for_sex.txt', [1, 0]), ('blame_washington_financial.txt', [1, 0]), \
('art_market_ethical.txt', [1, 0]), ('carbon_reductions_not_worth_it.txt', [1, 0]), ('bush_is_worst.txt', [0, 1]), \
('google_dont_be_evil.txt', [1, 0]), ('guns_reduce_crime.txt', [1, 0]), ('america_winning_iraq.txt', [1, 0]), \
('universal_health.txt', [0, 1]), ('legalize_organs.txt', [1, 0]), ('islam_radicals.txt', [1, 0]), \
('tough_interrogation.txt', [0, 1]), ('america_policeman.txt', [1, 0]), ('performance_enhancing.txt', [1, 0]), \
('aid_africa_bad.txt', [0, 1]), ('end_affirmative.txt', [0, 1]), ('russia_enemy_again.txt', [0, 1]), \
('stop_welcoming_immigrants.txt', [1, 0]), ('spread_democracy_me.txt', [1, 0]), ('booming_china.txt', [0, 1]), \
('more_domestic_surveillance.txt', [0, 1]), ('global_warming_not.txt', [1, 0]), ('america_too_religious.txt', [1, 0]), \
('hollywood_anti_us.txt', [0, 1]), ('democratic_hamas.txt', [0, 1]), ('license_to_offend.txt', [1, 0]), \
('tolerate_iran.txt', [1, 0])]

wordnet = WordNetLemmatizer()
stop = set(stopwords.words('english'))
all_words = [] 

for document in names_and_win:
    for_, aga_=  processing.parse_text('debate_text/'+document[0]) #/document

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

#print cosine_similarities
for index, vector in enumerate(tfidfed): 
    if sum(vector) == 0.0:
        print index 

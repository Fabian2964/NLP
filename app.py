#!/usr/bin/env python
# coding: utf-8

# In[5]:

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models, similarities, matutils
import re
import string
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4N6AV78lhdai8FnkNP5TTJvlvLzQqAAa3AM527sksFy1MC-g7Oj3jbt1E_1rKt2oaAQ&usqp=CAU", width=200)
# Title
st.header("Article Visits Prediction")

st.write("Please enter Article Characteristics to receive the estimated visits of your article")

# Input bar 1
body = st.text_area('Copy-Paste Article Text')

values_ressort = ['<select>','Finanzen', 'Gesellschaft', 'Karriere', 'Reise', 'Rhein-Main', 'Stil', 'Technik', 'Wirtschaft', 'Other']
default_ressort = values_ressort.index('<select>')

# Dropdown Input
ressort = st.selectbox('In which ressort is the article published?', values_ressort, index=default_ressort)

st.write('You selected:', ressort)

# Dropdown Input
read_time = st.number_input('What is the estimated reading time of the article (in minutes)?', step=1, min_value=0)

values_paid = ['<select>','Free', 'Dynamic', 'Paid']
default_paid = values_paid.index('<select>')

# Dropdown Input
paid = st.selectbox('Free, Dynamic or Paid?', values_paid, index=default_paid)

list_authors = ['<select>','alex_westhoff',
 'berthold_kohler',
 'christoph_schütte',
 'claudia_schülke',
 'dennis_kremer',
 'eva_maria_magel',
 'florentine_fritzen',
 'florian_balke',
 'franz_nestler',
 'fridtjof_küchemann',
 'friedrich_schmidt',
 'guido_holze',
 'hans_dieter_erlenbach',
 'hendrik_ankenbrand',
 'jan_hauser',
 'jan_schiefenhövel',
 'jasper_von_altenbockum',
 'julia_löhr',
 'jörg_daniels',
 'katharina_deschka',
 'katja_sturm',
 'kim_björn_becker',
 'markus_schug',
 'markus_wehner',
 'nikolas_busse',
 'thomas_gutschker',
 'tilman_spreckelsen',
 'volker_looman', 
 'Other']

default_author = list_authors.index('<select>')

# Dropdown Input
author = st.selectbox('Author', list_authors, index=default_author)

values_author_link = ['<select>','yes', 'no']
default_author_link = values_author_link.index('<select>')

# Dropdown Input
author_link = st.selectbox('Is a Link to Authors personal site included?', values_author_link, index=default_author_link)

values_source = ['<select>','news_agency', 'online', 'sunday_print']
default_source = values_source.index('<select>')

# Dropdown Input
source = st.selectbox('What is the article source?', values_source, index=default_source)

values_pub_day = ['<select>','Monday', 'Tuesday to Wednesday', 'Weekend', 'Other']
default_pub_day = values_pub_day.index('<select>')

# Dropdown Input
pub_day = st.selectbox('On which day is the article published?', values_pub_day, index=default_pub_day)

values_pub_time = ['<select>','11am-4pm', '4pm-9pm', 'Other']
default_pub_time = values_pub_time.index('<select>')

# Dropdown Input
pub_time = st.selectbox('Which time is the article published?', values_pub_time, index=default_pub_time)

nltk.download('stopwords')
list_sw = stopwords.words("german")
additional_sw = ['sagt', 'sei', 'seit', 'im', 'zwei', 'gibt', 'muss', 'tag', 'ganz', 'etwa', 'konnt', 'wurd', 'seien', 'beim', 'imm', 'erst', 'ganz', 'hatt', 'word', 'eig', 'bei', 'jahr', 'mehr', 'zahl', 'gut', 'mal', 'dafur', 'macht', 'mal', 'moglich', 'schon', 'hoh', 'dabei', 'geht', 'rund', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'million', 'milliard']

columns = ['labelpaid',
 'author_link',
 'dynamic',
 'jan_hauser',
 'katja_sturm',
 'thomas_gutschker',
 'julia_löhr',
 'fridtjof_küchemann',
 'markus_schug',
 'florentine_fritzen',
 'markus_wehner',
 'volker_looman',
 'nikolas_busse',
 'jasper_von_altenbockum',
 'christoph_schütte',
 'jan_schiefenhövel',
 'dennis_kremer',
 'jörg_daniels',
 'hendrik_ankenbrand',
 'guido_holze',
 'kim_björn_becker',
 'alex_westhoff',
 'hans_dieter_erlenbach',
 'franz_nestler',
 'friedrich_schmidt',
 'florian_balke',
 'tilman_spreckelsen',
 'katharina_deschka',
 'berthold_kohler',
 'claudia_schülke',
 'eva_maria_magel',
 'brightness',
 'rt_3_5',
 'rt_6_8',
 'rt_u8',
 'ressort_finanzen',
 'ressort_gesellschaft',
 'ressort_karriere_hochschule',
 'ressort_reise',
 'ressort_rhein_main',
 'ressort_stil',
 'ressort_technik_motor',
 'ressort_wirtschaft',
 'source_news_agency',
 'source_online',
 'source_sunday_print',
 'monday',
 'tues_thursday',
 'weekend',
 'time_11_16',
 'time_16_21',
 'time_21_06',
 'color_red']

stopwords_added = list_sw + additional_sw

nltk.download('punkt')

stemmer = SnowballStemmer("german")
stop_words = set(stopwords_added)


def clean_text(text, for_embedding=False):
    """
        - remove any html tags (< /br> often found)
        - Keep only ASCII + European Chars and whitespace, no digits
        - remove single letter chars
        - convert all whitespaces (tabs etc.) to single wspace
        if not for embedding (but e.g. tdf-idf):
        - all lowercase
        - remove stopwords, punctuation and stemm
    """
    RE_WSPACE = re.compile(r"\s+", re.IGNORECASE)
    RE_TAGS = re.compile(r"<[^>]+>")
    RE_ASCII = re.compile(r"[^A-Za-zÀ-ž ]", re.IGNORECASE)
    RE_SINGLECHAR = re.compile(r"\b[A-Za-zÀ-ž]\b", re.IGNORECASE)
    if for_embedding:
        # Keep punctuation
        RE_ASCII = re.compile(r"[^A-Za-zÀ-ž,.!? ]", re.IGNORECASE)
        RE_SINGLECHAR = re.compile(r"\b[A-Za-zÀ-ž,.!?]\b", re.IGNORECASE)

    text = re.sub(RE_TAGS, " ", text)
    text = re.sub(RE_ASCII, " ", text)
    text = re.sub(RE_SINGLECHAR, " ", text)
    text = re.sub(RE_WSPACE, " ", text)

    word_tokens = word_tokenize(text)
    words_tokens_lower = [word.lower() for word in word_tokens]

    if for_embedding:
        # no stemming, lowering and punctuation / stop words removal
        words_filtered = word_tokens
    else:
        words_filtered = [
            stemmer.stem(word) for word in words_tokens_lower if word not in stop_words
        ]

    
    words_filtered_refined = [word for word in words_filtered if word not in stop_words]
        
    text_clean = " ".join(words_filtered_refined)
    return text_clean
    


# If button is pressed
if st.button('Submit'):
    
    # Unpickle classifier
    rf = pickle.load(open('rf_visit_prediction.pkl','rb')) 
    
    
    lda = joblib.load('rf_lda_fitted.pkl')
    df_data_test = pd.read_csv('df_data_test_app.csv')
    df_data_test.drop('Unnamed: 0', axis=1, inplace=True)
    
    dic_temp = {}
    for i in columns:
    	dic_temp[i] = 0
    body = clean_text(body)
    dic_temp['text_full'] = body
    dic_temp['brightness'] = 118.77269637620297
    ressort_dict = {'Finanzen': 'ressort_finanzen','Gesellschaft': 'ressort_gesellschaft', 'Karriere': 'ressort_karriere_hochschule', 'Reise': 'ressort_reise', 'Rhein-Main': 'ressort_rhein_main', 'Stil': 'ressort_stil', 'Technik': 'ressort_technik_motor', 'Wirtschaft': 'ressort_wirtschaft'}
    try:
    	dic_temp[ressort_dict[ressort]] = 1
    except:
    	pass
    
    if (int(read_time) >2) & (int(read_time) <6):
    	dic_temp['rt_3_5'] = 1 
    elif ((int(read_time) >6) & (int(read_time) <9)):
    	dic_temp['rt_6_8'] = 1
    else:
    	if(int(read_time) >8):
    		dic_temp['rt_u8'] = 1
    
    if paid == 'Paid':
    	dic_temp['labelpaid'] = 1
    else:
    	if paid == 'Dynamic':
    		dic_temp['dynamic'] = 1
    		
    if author != '<select>':
    	dic_temp[author] = 1  
    
    if author_link == 'yes':
    	dic_temp['author_link'] = 1
    
    if source == 'news_agency':
    	dic_temp['source_news_agency'] = 1
    elif source == 'online':
    	dic_temp['source_online'] = 1
    else:
    	dic_temp['source_sunday_print'] = 1
    
    if pub_day == 'Monday':
    	dic_temp['monday'] = 1
    elif pub_day == 'Tuesday to Wednesday':
    	dic_temp['tues_thursday'] = 1
    else:
    	if pub_day == 'Weekend':
    		dic_temp['weekend'] = 1
    
    if pub_time == '11am-4pm':
    	dic_temp['time_11_16'] = 1
    else:
    	if pub_time == '4pm-9pm':
    		dic_temp['time_16_21'] = 1
    
    X = pd.DataFrame(dic_temp, index=[0])    
    
    pre_test = pd.concat([X, df_data_test], axis=0)
    pre_test.reset_index(drop=True, inplace=True)
    
    try:
    	pre_test = pre_test.drop(['date', 'year_month'], axis=1)
    except:
    	pass
    
    pre_test = pre_test.drop('log_visits', axis=1)
    df = pre_test['text_full']
    tv = TfidfVectorizer(min_df=.01, max_df=0.7, ngram_range=(1,2))
    X_tv_tr = tv.fit_transform(df).transpose()
    corpus_gensim_tv = matutils.Sparse2Corpus(X_tv_tr)
    
    lda_corpus_tv = lda[corpus_gensim_tv]
    lda_docs_tv = [doc for doc in lda_corpus_tv]
    
    topic_names = {}
    for i in range(7):
    	topic_names[i] = str(i)     
    topic_dic = dict()
    
    for i in topic_names.keys():
    	topic_dic[i] = []
    
    temp_list = []
    for i in range(7):
    	temp_list.append(i)
    
    set_topics = set(temp_list)
    
    for i in lda_docs_tv:
    	temp = []
    	for j in i:
    		temp.append(j[0])
    	for k in set_topics:
    		if k in temp:
    			continue
    		else:
    			topic_dic[k].append(0)
    	for l,m in i:
    		topic_dic[l].append(m)
    topic_names_cols = topic_names.copy()
    
    for i in topic_names_cols:
    	topic_names_cols[i]= 'topic_prob_' + topic_names_cols[i]
    
    topic_probs = pd.DataFrame(topic_dic).rename(columns=topic_names_cols)[0:1]
    
    cv_X_val = pd.concat([pre_test.iloc[0:1], topic_probs], axis=1)
    cv_X_val.drop('text_full', axis=1, inplace=True)
    
    # cv_X_val.drop('log_visits', axis=1, inplace=True)    
    dic_final = {}
    
    for i in cv_X_val.to_dict():
    	dic_final[i] = cv_X_val.to_dict()[i][0]
    	
    dct = {k:[v] for k,v in dic_final.items()}  # WORKAROUND
    df_final = pd.DataFrame(dct)
   
    # Get prediction
    prediction = np.exp(rf.predict(df_final))
    prediction = np.round(prediction, 0)
    
    # Output prediction
    st.text(f'This Article will generate {prediction} Visits.')


# In[ ]:





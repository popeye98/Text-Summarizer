#!/usr/bin/env python
# coding: utf-8

# In[4]:


import nltk
import re

import math
import operator

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
Stopwords=set(stopwords.words('english'))
wordlemmatizer=WordNetLemmatizer()


# In[5]:


def remove_special_characters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text


# In[6]:


def lemmatize_words(words):
    lemmatized_words = []
    for word in words:
       lemmatized_words.append(wordlemmatizer.lemmatize(word))
    return lemmatized_words


# In[7]:


def stem_words(words):
    stemmed_words = []
    for word in words:
       stemmed_words.append(stemmer.stem(word))
    return stemmed_words


# In[14]:


def clean_text(text):
    tokenized_sentence=sent_tokenize(text)
    text=remove_special(text)
    text = re.sub(r'\d+', '', text)
    tokenized_words=word_tokenize(text)
    tokenized_words=[word for word in tokenized_words if word not in Stopwords]
    tokenized_words=[word for word in tokenized_words if len(word)>1]
    tokenized_words=[word.lower() for word in tokenized_words]
    return tokenized_words
    


# In[15]:


def calc_freq(words):
    words = [word.lower() for word in words]
    dict_freq = {}
    words_unique = []
    for word in words:
       if word not in words_unique:
           words_unique.append(word)
    for word in words_unique:
       dict_freq[word] = words.count(word)
    return dict_freq


# In[ ]:





# In[19]:


#https://www.geeksforgeeks.org/part-speech-tagging-stop-words-using-nltk-python/


# In[20]:


def pos_tagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
             pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb


# In[21]:


pos_tagging('Sukanya, Rajib and Naba are my good friends')


# If a word appears frequently in a document, then it should be important and we should give that word a high score. But if a word appears in too many other documents, it’s probably not a unique identifier, therefore we should assign a lower score to that word.
# 
# 
#     Formula for calculating tf and idf:
# 
#     TF(w) = (Number of times term w appears in a document) / (Total number of terms in the document)
# 
#     IDF(w) = log_e(Total number of documents / Number of documents with term w in it)
# 
#     Hence tfidf for a word can be calculated as:
# 
#     TFIDF(w) = TF(w) * IDF(w)

# In[22]:


def tf_score(word,sentence):
    freq_sum = 0
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf =  word_frequency_in_sentence/ len_sentence
    return tf


# In[23]:


def idf_score(no_of_sentences,word,sentences):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        sentence = remove_special_characters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.split()
        sentence = [word for word in sentence if word.lower() not in Stopwords and len(word)>1]
        sentence = [word.lower() for word in sentence]
        sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
        if word in sentence:
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
    return idf


# In[24]:


def tf_idf_score(tf,idf):
    return tf*idf


# In[ ]:





# In[25]:


def word_tfidf(dict_freq,word,sentences,sentence):
    word_tfidf = []
    tf = tf_score(word,sentence)
    idf = idf_score(len(sentences),word,sentences)
    tf_idf = tf_idf_score(tf,idf)
    return tf_idf


# In[26]:


def sentence_importance(sentence,dict_freq,sentences):
     sentence_score = 0
     sentence = remove_special_characters(str(sentence)) 
     sentence = re.sub(r'\d+', '', sentence)
     pos_tagged_sentence = [] 
     no_of_sentences = len(sentences)
     pos_tagged_sentence = pos_tagging(sentence)
     for word in pos_tagged_sentence:
          if word.lower() not in Stopwords and word not in Stopwords and len(word)>1: 
                word = word.lower()
                word = wordlemmatizer.lemmatize(word)
                sentence_score = sentence_score + word_tfidf(dict_freq,word,sentences,sentence)
     return sentence_score


# In[27]:


text='''Women education is a catch all term which refers to the state of primary, secondary, tertiary and health education in girls and women. There are 65 Million girls out of school across the globe; majority of them are in the developing and underdeveloped countries. All the countries of the world, especially the developing and underdeveloped countries must take necessary steps to improve their condition of female education; as women can play a vital role in the nation’s development.
If we consider society as tree, then men are like its strong main stem which supports the tree to face the elements and women are like its roots; most important of them all. The stronger the roots are the bigger and stronger the tree will be spreading its branches; sheltering and protecting the needy.
Women are the soul of a society; a society can well be judged by the way its women are treated. An educated man goes out to make the society better, while an educated woman; whether she goes out or stays at home, makes the house and its occupants better.
Women play many roles in a society- mother, wife, sister, care taker, nurse etc. They are more compassionate towards the needs of others and have a better understanding of social structure. An educated mother will make sure that her children are educated, and will weigh the education of a girl child, same as boys.
History is replete with evidences, that the societies in which women were treated equally to men and were educated; prospered and grew socially as well as economically. It will be a mistake to leave women behind in our goal of sustainable development, and it could only be achieved if both the genders are allowed equal opportunities in education and other areas.
Education makes women more confident and ambitious; they become more aware of their rights and can raise their voice against exploitation and violence. A society cannot at all progress if its women weep silently. They have to have the weapon of education to carve out a progressive path for their own as well as their families.'''


# In[37]:


def process(text,input_user):


    tokenized_sentence = sent_tokenize(text)
    text = remove_special_characters(str(text))
    text = re.sub(r'\d+', '', text)
    tokenized_words_with_stopwords = word_tokenize(text)
    tokenized_words = [word for word in tokenized_words_with_stopwords if word not in Stopwords]
    tokenized_words = [word for word in tokenized_words if len(word) > 1]
    tokenized_words = [word.lower() for word in tokenized_words]
    tokenized_words = lemmatize_words(tokenized_words)
    word_freq = calc_freq(tokenized_words)
   
    no_of_sentences = int((input_user * len(tokenized_sentence))/100)
    print(no_of_sentences)
    c = 1
    sentence_with_importance = {}
    for sent in tokenized_sentence:
        sentenceimp = sentence_importance(sent,word_freq,tokenized_sentence)
        sentence_with_importance[c] = sentenceimp
        c = c+1
    sentence_with_importance = sorted(sentence_with_importance.items(), key=operator.itemgetter(1),reverse=True)
    cnt = 0
    summary = []
    sentence_no = []
    for word_prob in sentence_with_importance:
        if cnt < no_of_sentences:
            sentence_no.append(word_prob[0])
            cnt = cnt+1
        else:
          break
    sentence_no.sort()
    cnt = 1
    for sentence in tokenized_sentence:
        if cnt in sentence_no:
           summary.append(sentence)
        cnt = cnt+1
    summary = " ".join(summary)
    return summary
        
    


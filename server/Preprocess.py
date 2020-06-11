# -*- coding: utf-8 -*-
import Stemmer
import json
import time

inverted_index = dict()
stoplist_file = "stoplist.txt"
aditional_characters = "áéíóúÁÉÍÓÚñÑ"
stopwords = []
stemmer = Stemmer.Stemmer('spanish')


def load_step_words():
    with open(stoplist_file, 'r') as fdata:
        lines = fdata.readlines()
        for x in lines:
            stopwords.append(x.strip())
    stopwords.append("rt")
    stopwords.append("ci")


def clean_word(word):
    new_word = ""
    for c in word:
        if c == '@' or c == '#':
            return ""
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c in aditional_characters:
            new_word += c

    return new_word.lower()


def tokenize(text):
    tokens = []
    text = text.split(' ')
    for word in text:
        word = clean_word(word)
        if word not in stopwords and word != "":
            tokens.append(word)
    return tokens


def stemming(tokens):
    return stemmer.stemWords(tokens)


def pre_process(data):
    stime = time.time()
    for ifile in data.values():
        ifile_data = json.loads(ifile.read())
        i =0
        for tweet in ifile_data:
            tokens = tokenize(tweet['text'])
            stems = stemming(tokens)
            for stem in stems:
                if stem in inverted_index:
                    inverted_index[stem].add(tweet['id'])
                else:
                    inverted_index[stem] = {tweet['id']}
    etime = time.time()
    print("Finish preprocess")
    print("----%s seconds"%(etime-stime))
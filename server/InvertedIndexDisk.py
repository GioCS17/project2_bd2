# -*- coding: utf-8 -*-
from os import listdir
from os.path import isfile, isdir
import json
import io
import os
import glob
import time
from Preprocess import tokenize, stemming, load_step_words


path_files = './files/'


class Document:
    def __init__(self, text, idx):
        self.text = text.lower()
        self.id = idx


class InvertedIndex:
    def __init__(self):
        self.words = []
        self.filename = 'initial.txt'
        self.runs_files = 0

    def process(self, documents):
        file = open(path_files + self.filename, 'w')
        file_words = open(path_files + 'words.txt', 'w')
        for d in documents:
            #text = d.text.replace(',', '').split(" ")
            text = stemming(tokenize(d.text))
            words_doc = []
            for t in text:
                t = t
                if not (t in words_doc):
                    words_doc.append(t)
                    if not (t in self.words):
                        self.words.append(t)
                        file_words.write(str(self.words.index(t) + 1) + ',' + str(t) + '\n')
                    idx = self.words.index(t)
                    f = text.count(t)
                    file.write(str(idx + 1) + ',' + str(d.id) + ',' + str(f) + '\n')
        file_words.close()
        file.close()

    def sort_runs(self, k):
        file1 = open(path_files + self.filename, 'r')
        run = []
        idx_run = 1
        for line in file1.read().split('\n'):
            record = line.split(',')
            if len(record) == 3:
                run.append(record)
                if len(run) == k:
                    file_run = open(path_files + str(idx_run) + 'run.txt', 'w')
                    run = sorted(run, key=lambda term: int(term[0]))
                    for r in run:
                        file_run.write(str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '\n')
                    file_run.close()
                    idx_run += 1
                    self.runs_files += 1
                    run = []
        if len(run) < k:
            file_run = open(path_files + str(idx_run) + 'run.txt', 'w')
            run = sorted(run, key=lambda term: int(term[0]))
            for r in run:
                file_run.write(str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '\n')
            file_run.close()
            self.runs_files += 1
        file1.close()

    def merging(self):
        l = []
        for i in range(self.runs_files):
            file_run = open(path_files + str(i + 1) + 'run.txt', 'r')
            l = l + list(file_run)
            file_run.close()
        l = sorted(l, key=lambda term: int(term.split(',')[0]))
        c = ''.join(l)
        file_final = open(path_files + "final.txt", 'w')
        file_final.write(c)
        file_final.close()


def create_twitter(data):


    load_step_words()
    #path = './clean/'
    #archivos = [obj for obj in listdir(path) if isfile(path + obj)]
    docs = []
    stime = time.time()
    for ifile in data.values():
        ifile_data = json.loads(ifile.read())
        i = 0
        for tweet in ifile_data:
            new_doc = Document(tweet["text"], tweet["id"])
            docs.append(new_doc)
    '''for arch in archivos:
        with io.open('./clean/' + arch, 'r', encoding="utf-8") as data_file:
            json_data = data_file.read()
        data = json.loads(json_data)
        for t in data:
            new_doc = Document(t["text"], t["id"])
            docs.append(new_doc)
        if len(docs) > 20:
            break'''
    ii = InvertedIndex()
    ii.process(docs)
    ii.sort_runs(10)
    ii.merging()
    return "created"


def generate_index():
    index = {}
    in_ind = open(path_files + 'final.txt', 'r').read().split('\n')
    for ind in in_ind:
        dic = ind.split(',')
        if len(dic) == 3:
            word_id = int(dic[0])
            doc_id = int(dic[1])
            freq = int(dic[2])
            doc_freq = (doc_id, freq)
            if word_id in index:
                index[word_id].append(doc_freq)
            else:
                new_ind = [doc_freq]
                index[word_id] = new_ind

    return index
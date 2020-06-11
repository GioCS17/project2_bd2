from flask import Flask
from flask import render_template 
from flask import request
from flask import jsonify
import json
import Stemmer
import time

path = "./../"

app = Flask(__name__)

inverted_index = dict()
stoplist_file="stoplist.txt"
aditional_characters= "áéíóúÁÉÍÓÚñÑ"
stopwords=[]
stemmer=Stemmer.Stemmer('spanish')

def loadStepWords():
    with open(stoplist_file, 'r', encoding='utf8',errors='surrogateescape') as fdata:
        lines = fdata.readlines();
        for x in lines:
            stopwords.append(x.strip())
    stopwords.append("rt")
    stopwords.append("ci")

def clean_word(word):
    new_word=""
    for c in word:
        if c=='@' or c=='#':
            return ""
        if 'a'<=c<='z' or 'A'<=c<='Z' or c in aditional_characters:
            new_word+=c

    return new_word.lower()

def tokenize(text):
    tokens=[]
    #print(text)
    text=text.split(' ')
    for word in text:
        word=clean_word(word)
        if word not in stopwords and word!="":
            tokens.append(word)
    return tokens

def stemming(tokens):
    return stemmer.stemWords(tokens)


def preprocess(data):
    stime=time.time()
    for ifile in data.values():
        ifile_data=json.loads(ifile.read())
        i =0
        for tweet in ifile_data:
            tokens=tokenize(tweet['text'])
            #print(tokens)
            stems=stemming(tokens)
            #print(stems)
            for stem in stems:
                if stem in inverted_index:
                    inverted_index[stem].add(tweet['id'])
                else:
                    inverted_index[stem]={tweet['id']}
    etime=time.time()
    print("Finish preprocess")
    print("----%s seconds"%(etime-stime))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload",methods=['POST'])
def getRamsin():
    print("entro a upload")
    data = dict(request.files)
    preprocess(data)


    return jsonify({'status':201}) 

if __name__=="__main__":
    loadStepWords()
    app.run(debug=True)
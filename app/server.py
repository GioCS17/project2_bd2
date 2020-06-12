from flask import Flask
from flask import render_template 
from flask import request
from flask import jsonify
import math
import json
from flask_cors import CORS
import params
import tweepy
from Preprocess import tokenize, stemming, pre_process
from InvertedIndexDisk import Document, create_twitter, generate_index

# instantiate the app
app = Flask(__name__)
#app.config.from_object(__name__)

path_files = './files/'


# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/tweets/<text>', methods=['GET'])
def search_tweets(text):
    words = open(path_files + 'words.txt', 'r').read().split('\n')
    #in_ind = open(path_files + 'final.txt', 'r').read().split('\n')
    text_sep = stemming(tokenize(text))
    documents = {}
    my_index, num_docs = generate_index()
    for word in words:
        word_data = word.split(',')
        if len(word_data) == 2:
            word_index = int(word_data[0])
            word_data = word_data[1]
            if word_data in text_sep:
                if word_index in my_index:
                    docs_info = my_index.get(word_index)
                    idf = math.log((num_docs / (len(docs_info))), 10)
                    for doc_info in docs_info:
                        tf = math.log(1 + doc_info[1], 10)
                        tf_idf = tf * idf
                        if doc_info[0] in documents:
                            documents[doc_info[0]] += tf_idf
                        else:
                            documents[doc_info[0]] = tf_idf
                        #if not (doc_info[0] in documents):
                         #   documents.append(doc_info[0])

    docs_json = []

    auth = tweepy.OAuthHandler(params.consumer_key, params.consumer_secret)
    auth.set_access_token(params.access_token, params.access_token_secret)

    api = tweepy.API(auth)
    datos = ['created_at']
    user_datos = ['name', 'screen_name', 'location', 'profile_image_url']

    for d in documents:
        id = int(d)
        score = documents[d]
        try:
            status = api.get_status(id, tweet_mode="extended")
            s = status.__dict__
            tweet = {'id': d, 'text': s['full_text']}
            for d in datos:
                if d in s:
                    tweet[d] = s[d]
            author = s['author'].__dict__
            for d in user_datos:
                if d in author:
                    tweet[d] = author[d]
            tweet['score'] = score
            docs_json.append(tweet)
        except tweepy.TweepError:
            print("Failed to run the command on that tweet, Skipping...")
    return jsonify(docs_json)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload",methods=['POST'])
def getRamsin():
    print("entro a upload")
    data = dict(request.files)
    create_twitter(data)
    print("hey")

    return jsonify({'status': 201})


if __name__=="__main__":
    app.run(debug=True)
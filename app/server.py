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
CORS(app, resources={r'/*': {'origins': '*'}})

my_index={}
num_docs = 0

@app.route('/tweets/<text>', methods=['GET'])
def search_tweets(text):
    print("start searching")
    global my_index
    global num_docs
    words = open(path_files + 'words.txt', 'r').read().split('\n')
    #in_ind = open(path_files + 'final.txt', 'r').read().split('\n')
    text_sep = stemming(tokenize(text))
    documents = {}
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

    print("end searching")

    auth = tweepy.OAuthHandler(params.consumer_key, params.consumer_secret)
    auth.set_access_token(params.access_token, params.access_token_secret)

    api = tweepy.API(auth)
    datos = ['created_at']
    user_datos = ['name', 'screen_name', 'location', 'profile_image_url']
    tweets_no_count = 0
    for d in documents:
        id = int(d)
        score = documents[d]
        try:
            status = api.get_status(id, tweet_mode="extended")
            s = status.__dict__
            author = s['author'].__dict__
            tweet = {'id': id, 'text': s['full_text'], 'created_at': s['created_at'], 'name': author['name'],
                     'screen_name': author['screen_name'], 'location': author['location'],
                     'profile_image_url': author['profile_image_url'], 'score': score}
            docs_json.append(tweet)
        except tweepy.TweepError:
            tweets_no_count += 1
    return jsonify(docs_json)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload",methods=['POST'])
def getRamsin():
    print("entro a upload")
    data = dict(request.files)
    create_twitter(data)
    global my_index
    global num_docs
    my_index, num_docs = generate_index()
    print("hey")

    return jsonify({'status': 201})


if __name__=="__main__":
    app.run(debug=True)
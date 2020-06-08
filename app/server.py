from flask import Flask
from flask import render_template 
from flask import request
from flask import jsonify
import json

path = "./../"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload",methods=['POST'])
def getRamsin():
    print("entro a upload")
    #request_data = json.loads(request.get_data())
    request_data=request.files
    data =request_data['json0'].read()
    #data_prev= data.decode('utf8').replace("'", '"')
    data_json = json.loads(data)
    #print(type(data_json))
    #print(data_json)
    for i in range(1):
        print(data_json[i])
    return jsonify({'status':201}) 

if __name__=="__main__":
    app.run(debug=True)
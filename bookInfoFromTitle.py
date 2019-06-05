import flask
import math
import numpy as np
import pandas as pd
import requests
import xmltodict
import pprint
import json
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/book/', methods=['POST'])
def home():
    name=request.values.get("title")
    info=[]
    def getBookInfo(title):
        import numpy as np
        import pandas as pd
        import requests
        import xmltodict
        
        import json
        url=' https://www.goodreads.com/book/title.xml'
        parameters={"key":' laszLDheUrLhOPhB43g',"title":title}
        result = requests.get(url,params=parameters)
        my_dict = xmltodict.parse(result.content)
        x=my_dict['GoodreadsResponse']['book']
        if 'id' in x:
            idb=x['id']
        url='https://www.goodreads.com/book/show.xml'
        parameters={"key":' laszLDheUrLhOPhB43g',"id":idb}
        result = requests.get(url,params=parameters)
        my_dict = xmltodict.parse(result.content)
        x=my_dict['GoodreadsResponse']['book']
        info.append("Title : {}".format(x['title']))
        info.append("Book id :{}".format(idb))
        info.append(x['image_url'])
        info.append("Averge Rating : {}".format(x['average_rating']))
        info.append("Author : {}".format(x['authors']['author']['name']))
    getBookInfo(name)
    return jsonify(info)
app.run()
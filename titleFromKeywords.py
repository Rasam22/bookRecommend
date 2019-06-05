import flask
import math
import numpy as np
import pandas as pd
import requests
import xmltodict
import json
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/book/', methods=['POST'])
def home():
    keyword=request.values.get("string")
    info=[]
    def getInfo(key):
        import numpy as np
        import pandas as pd
        import requests
        import xmltodict
        import pprint
        import json
        url=' https://www.goodreads.com/search/index.xml'
        parameters={"key":' laszLDheUrLhOPhB43g',"q":key}
        result = requests.get(url,params=parameters)
        my_dict = xmltodict.parse(result.content)
        x=my_dict['GoodreadsResponse']['search']['results']['work']
        for i in x:
            ans=i['best_book']
            info.append(ans['title'])
    getInfo(keyword)
    return jsonify(info)

app.run()
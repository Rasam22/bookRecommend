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
    title1=request.values.get("title1")
    title2=request.values.get("title2")
    title3=request.values.get("title3")
    publication=[]
    rating=[]
    reviewsS=[]
    reviewsO=[]
    reviews=[]
    distance=[]
    publYrS=[]
    ratingS=[]
    publYrO=[]
    page=[]
    pagesO=[]
    pagesS=[]
    ratingO=[]
    titles=[]
    def getSimilarBooks(title):
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
        tempt=my_dict['GoodreadsResponse']['book']['title']
        tempi=my_dict['GoodreadsResponse']['book']['id']
        if 'publication_year' in x:
            publicationYear=my_dict['GoodreadsResponse']['book']['publication_year']
        if 'average_rating' in x:
            ratingsAvg=my_dict['GoodreadsResponse']['book']['average_rating']
        if 'num_pages' in x:
            pages=my_dict['GoodreadsResponse']['book']['num_pages']
        if 'reviews_count' in x['work']:
            review=my_dict['GoodreadsResponse']['book']['work']['reviews_count']['#text']
        if 'similar_books' in x:
            ans=my_dict['GoodreadsResponse']['book']['similar_books']['book']
            cnt=0;
            for j in ans:
                flag=0
                if cnt<5:
                    idb1=j['id']
                    title=j['title']
                    df=pd.read_csv('reject.csv')
                    for i,row in df.iterrows():
                        if row["names"]==title:
                            flag=1
                            break
                    for i in range(len(titles)):
                        if titles[i]==title:
                            flag=1
                            break
                    if flag==0:
                        titles.append(j['title'])
                        if j['publication_year'] != None:
                            publYrS.append(int(j['publication_year']))
                        else:
                            publYrS.append(0)               
                        if j['average_rating'] != None:
                            ratingS.append(float(j['average_rating']))
                        else:
                            ratingS.append(0)
                        if j['num_pages'] != None:
                            pagesS.append(int(j['num_pages']))
                        else:
                            pagesS.append(0)
                        cnt=cnt+1
                        url='https://www.goodreads.com/book/show.xml'
                        parameters={"key":' laszLDheUrLhOPhB43g',"id":idb1}
                        result = requests.get(url,params=parameters)
                        my_dict = xmltodict.parse(result.content)
                        x=my_dict['GoodreadsResponse']['book']['work']
                        reviewsS.append(int(x['reviews_count']['#text']))

        else:
            print('no similar books exist')
        
        if publicationYear != None:
            publYrO.append(int(publicationYear))
        else:
            publYrO.append(0)
        if ratingsAvg != None:
            ratingO.append(float(ratingsAvg))
        else:
            ratingO.append(0)
        if pages != None:
            pagesO.append(int(pages))
        else:
            pagesO.append(0)
        if review != None:
            reviewsO.append(int(review))
        else:
            reviewsO.append(0)
    
    def userChoice(title1,title2,title3):
        getSimilarBooks(title1);
        getSimilarBooks(title2);
        getSimilarBooks(title3);

    userChoice(title1,title2,title3)

    def distanceCalculation():
        x=len(publYrS)
        x1=publYrO[0]
        x2=publYrO[1]
        x3=publYrO[2]
        for i in range(x):
            dist=math.sqrt((publYrS[i]-x1)**2+(publYrS[i]-x2)**2+(publYrS[i]-x3)**2)
            publication.append(dist)
        y=len(ratingS)
        y1=ratingO[0]
        y2=ratingO[1]
        y3=ratingO[2]
        for i in range(y):
            dist=math.sqrt((ratingS[i]-y1)**2+(ratingS[i]-y2)**2+(ratingS[i]-y3)**2)
            rating.append(dist)   
        z=len(pagesS)
        z1=pagesO[0]
        z2=pagesO[1]
        z3=pagesO[2]
        for i in range(z):
            dist=math.sqrt((pagesS[i]-z1)**2+(pagesS[i]-z2)**2+(pagesS[i]-z3)**2)
            page.append(dist)
        w=len(reviewsS)
        w1=reviewsO[0]
        w2=reviewsO[1]
        w3=reviewsO[2]
        for i in range(w):
            dist=math.sqrt((reviewsS[i]-w1)**2+(reviewsS[i]-w2)**2+(reviewsS[i]-w3)**2)
            reviews.append(dist)

    distanceCalculation()

    yr=15
    rate=4
    pg=8
    rv=6
    x=len(rating)
    for i in range(x):
        dist=rating[i]*rate+publication[i]*yr+page[i]*pg+reviews[i]*rv
        distance.append(dist)

    for i in range(1,x):
        data=distance[i]
        book=titles[i]
        j=i-1
        while data<distance[j] and j>=0:
            distance[j+1]=distance[j]
            titles[j+1]=titles[j]
            j=j-1
        distance[j+1]=data
        titles[j+1]=book
    
    return jsonify(titles)


app.run()
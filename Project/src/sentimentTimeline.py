from pymongo import MongoClient
import certifi
from pprint import pprint
import plotly.express as px
import pandas as pd

ca = certifi.where()

client = MongoClient("mongodb+srv://jihnpk:240825Pass!@cs432.m5855.mongodb.net/proj3?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.proj3

serverStatusResult = db.command("serverStatus")
collection = db.twitterData

def dateParse(dateString):
    dateWords = []
    word = ''
    for c in dateString:
        if(c == ' '):
            dateWords.append(word)
            word = ''
        else:
            word += c
        
    dateWords.append(word)

    return {'month': dateWords[1], 'day': dateWords[2], 'year': dateWords[5]}

years = ['2020', '2021']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

sentimentValues = []
dateValues = []

for year in years:
    for month in months:
        if collection.find_one({'$and': [{'created_at': {'$regex': year}}, {'created_at': {'$regex': month}}]}) != None:
            dataset = collection.find({'$and': [{'created_at': {'$regex': year}}, {'created_at': {'$regex': month}}]})
            count = 0
            sentimentSum = 0.0
            for data in dataset:
                sentiment = data['sentiment']
                sentimentSum += sentiment
                count += 1;

            sentimentValues.append(sentimentSum/count)
            dateValues.append(month + ' ' + year)

print('done')

df = pd.DataFrame(dict(sentiment = sentimentValues, date = dateValues))

print(df)

fig = px.line(df, x='date', y='sentiment', labels = dict(
    date = 'Date (Month Year)',
    sentiment = 'Average Sentiment [-1, 1]'
), title = 'Average Twitter Sentiment From March 2020 to Sep 2021')
fig.write_html("sentimentOverTimeDays.html")
fig.show()

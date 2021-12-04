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

    words = [str(months.index(dateWords[1]) + 1), '/',dateWords[2],'/',dateWords[5]]

    return ''.join(words)

years = ['2021']
months = ['Jan']

countValues = []
sentimentValues = []
dateValues = []

for year in years:
    for month in months:
        print(month)
        if collection.find_one({'$and': [{'created_at': {'$regex': year}}, {'created_at': {'$regex': month}}]}) != None:
            dataset = collection.find({'$and': [{'created_at': {'$regex': year}}, {'created_at': {'$regex': month}}]})
            
            for data in dataset:
                sentimentVal = data['sentiment']
                dateVal = dateParse(data['created_at'])
                pprint(data)

                try:
                    valueIndex = dateValues.index(dateVal)

                    countValues[valueIndex] += 1
                    sentimentValues[valueIndex] += sentimentVal
                except ValueError:
                    dateValues.append(dateVal)
                    sentimentValues.append(sentimentVal)
                    countValues.append(0)
                
for i in range(len(dateValues)):
    sentimentValues[i] /= countValues[i]

df = pd.DataFrame(dict(
    x = dateValues,
    y = sentimentValues
))

print(df)

df['x'] = pd.to_datetime(df['x'])
df.sort_values(by = ['x'])

print(df)

fig = px.line(df, x = 'x', y = 'y', title = 'Average Twitter Sentimnet From March 2020 to Sep 2021')

fig.update_layout( xaxis_title = 'Month Year', yaxis_title='Average Sentiment [-1, 1]')

fig.write_html("sentimentOverTimeDays.html")
fig.show()

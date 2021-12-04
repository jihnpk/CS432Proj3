from pymongo import MongoClient
import certifi
from pprint import pprint

ca = certifi.where()

client = MongoClient("mongodb+srv://jihnpk:240825Pass!@cs432.m5855.mongodb.net/proj3?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.proj3

serverStatusResult = db.command("serverStatus")
twitterData = db.twitterData
parsedData = db.parsedData

dataset = twitterData.find()

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

print('starting to parse data')

for data in dataset:
    fullTextData = data['full_text']
    
    if (parsedData.find_one({'full_text': fullTextData}) == None):
        dateData = dateParse(data['created_at'])
        sentimentData = data['sentiment']
        coordinateData = data['coordinates']
        newData = {'date': dateData, 'full_text': fullTextData, 'sentiment': sentimentData, 'coordinates': coordinateData}
        x = parsedData.insert_one(newData)
        print('inserted')
        
    #else:
        #print('failed to insert')
        #print(str(coordinateData) + ' ' + str(fullTextData))
    

    
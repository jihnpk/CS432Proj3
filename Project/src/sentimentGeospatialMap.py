from pymongo import MongoClient
import certifi
from pprint import pprint
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

ca = certifi.where()

client = MongoClient("mongodb+srv://jihnpk:240825Pass!@cs432.m5855.mongodb.net/proj3?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.proj3

serverStatusResult = db.command("serverStatus")
collection = db.twitterData

dataset = collection.find()

sentimentValues = []
latitudes = []
longitudes = []

for data in dataset:
    coordinateData = data['coordinates']
    if(coordinateData != None):
        sentimentValues.append(data['sentiment'])
        latitudes.append(coordinateData['coordinates'][1])
        longitudes.append(coordinateData['coordinates'][0])

df = pd.DataFrame(dict(sentiment = sentimentValues, lat = latitudes, lon = longitudes))

fig = go.Figure(data=go.Scattergeo(
    lon = df['lon'],
    lat = df['lat'],
    text = df['sentiment'],
    mode = 'markers',
    marker = dict(
        size = 8,
        opacity = 0.8,
        reversescale = True,
        autocolorscale = False,
        symbol = 'square',
        line = dict(
            width=1,
            color='rgba(102, 102, 102)'
        ),
        colorscale = 'rdbu_r',
        color = df['sentiment'],
        cmin = df['sentiment'].min(),
        cmax = df['sentiment'].max(),
        colorbar_title="Twitter Sentiment Values<br>[-1,1]"
)))

fig.update_layout(
        title = 'Worldwide Sentiment Values<br>Hover for Values',
        geo = dict(
            scope='world',
            projection_type='natural earth',
            showland = True,
            landcolor = "rgb(190, 209, 195)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )

fig.write_html("sentimentScatterGeo.html")
fig.show()
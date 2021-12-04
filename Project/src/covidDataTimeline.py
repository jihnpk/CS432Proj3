from pymongo import MongoClient
import certifi
from pprint import pprint
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

ca = certifi.where()

client = MongoClient("mongodb+srv://jihnpk:240825Pass!@cs432.m5855.mongodb.net/proj3?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.proj3

serverStatusResult = db.command("serverStatus")
collection = db.covidData

covidDataset = collection.find()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

newDeaths = []
newCases = []
newVacc = []
dateValues = []

for data in covidDataset:
    for day in data['data']:

        if 'new_cases_smoothed' in day:
            newCasesNum = day['new_cases_smoothed']

        if 'new_deaths_smoothed' in day:
            newDeathsNum = day['new_deaths_smoothed']

        if 'new_people_vaccinated_smoothed' in day:
            newVaccNum = day['new_people_vaccinated_smoothed']

        try:
            valueIndex = dateValues.index(day['date'])
            if 'new_cases_smoothed' in day:
                newCases[valueIndex] += newCasesNum

            if 'new_deaths_smoothed' in day:
                newDeaths[valueIndex] += newDeathsNum

            if 'new_people_vaccinated_smoothed' in day:
                newVacc[valueIndex] += newVaccNum
        except ValueError:
            dateValues.append(day['date'])

            if 'new_cases_smoothed' in day:
                newCases.append(day['new_cases_smoothed'])
            else:
                newCases.append(0)

            if 'new_deaths_smoothed' in day:
                newDeaths.append(day['new_deaths_smoothed'])
            else:
                newDeaths.append(0)

            if 'new_people_vaccinated_smoothed' in day:
                newVacc.append(day['new_people_vaccinated_smoothed'])
            else:
                newVacc.append(0)

for i in range(146):            
    newDeaths.pop()
    newCases.pop()
    newVacc.pop()
    dateValues.pop()

for i in range(6):            
    newDeaths.pop(0)
    newCases.pop(0)
    newVacc.pop(0)
    dateValues.pop(0)

print(dateValues)

fig = go.Figure()

fig.add_trace(go.Scatter(x = dateValues, y = newDeaths, name = 'New Deaths', line = dict(
    color = 'firebrick', width = 4
)))

fig.add_trace(go.Scatter(x = dateValues, y = newCases, name = 'New Cases', line = dict(
    color = 'darkgreen', width = 4
)))

fig.add_trace(go.Scatter(x = dateValues, y = newVacc, name = 'New Vaccinations', line = dict(
    color = 'royalblue', width = 4
)))

fig.update_layout(title = 'Covid Data Trends', xaxis_title = 'Month Year', yaxis_title='')

fig.write_html("CovidData.html")
fig.show()
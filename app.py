from flask import Flask, render_template, request, escape
import pandas as pd
from collections import Counter
#import json

app=Flask(__name__)

def open_file ():
   data = pd.read_csv('locations.txt')
   return data.iloc[:, [1,2]]

def open_file_corp ():
   data = pd.read_csv('companiesdb.csv')
   return data

def open_file_blue ():
   data = pd.read_csv('bluetooth.csv')
   return data

def get_latlon():
   '''
    Function to get the map data
   '''
   markers = []
   ll_data = open_file()

   for index, row in ll_data.iterrows():
      markers.append({'lat': float(row[0]), 'lon': float(row[1])})

   return markers

def get_companies():
   '''
    Function to get the map data
   '''
   markers = []
   data = open_file_corp()
   ll_data = data[['Tag', 'Geo']]

   for index, row in ll_data.iterrows():
      geo = row['Geo'].split(',')
      markers.append({'lat': float(geo[0]), 'lon': float(geo[1]), 'tag':row['Tag']})

   return markers

def filter_types(iot_types):
   '''

   '''
   iot = []
   if ";" in iot_types:
      iot = iot_types.split(";")
   else:
      iot.append(iot_types)
   
   markers = []

   data = open_file_corp()
   company_data = data[data['Tag'].isin(iot)][['Tag', 'Geo']]

   for index, row in company_data.iterrows():
      geo = row['Geo'].split(',')
      markers.append({'lat': float(geo[0]), 'lon': float(geo[1]), 'tag':row['Tag']})

   return markers

   #blue = open_file_blue()
   #filtered_companies = blue[blue['Company'].isin(company_id)]

   #return filtered_companies

def filter_company_types (company):
   '''
   Get counts for tags by company
   '''
   counter_obj = Counter()
   for comp in company:
      counter_obj["\'" + comp['tag'] + "\'"] += 1

   dict = {str(k):v for k,v in counter_obj.items()}
   return dict


@app.route('/', methods = ['POST', 'GET'])
def root():
   if request.method == 'POST':
      filter_company = request.form['iotfilter']

      if filter_company == "":
         companies = get_companies()
      else:
         companies = filter_types(filter_company)
   else:   
      companies = get_companies()

   barplot = filter_company_types(companies)

   markers = get_latlon()
   setup=markers[0] 

   comp_setup={'lat':0, 'lon':0}  

   return render_template('index.html',markers=markers, setup=setup, 
      companies=companies, comp_setup=comp_setup, barplot=escape(barplot) )

@app.route('/company', methods = ['POST', 'GET'])
def company():
   if request.method == 'POST':
      filter_company = request.form['iotfilter']

      if filter_company == "":
         markers = get_companies()
      else:
         markers = filter_types(filter_company)
   else:
      markers = get_companies()
   setup={'lat':0, 'lon':0} 

   return render_template('companies.html',markers=markers, setup=setup )

if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)

from flask import Flask, render_template
import pandas as pd

app=Flask(__name__)

def open_file ():
   data = pd.read_csv('locations.txt')
   return data.iloc[:, [1,2]]

def open_file_corp ():
   data = pd.read_csv('companiesdb.csv')
   return data[['Tag', 'Geo']]

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
   ll_data = open_file_corp()
   print(ll_data.head())

   for index, row in ll_data.iterrows():
      geo = row['Geo'].split(',')
      markers.append({'lat': float(geo[0]), 'lon': float(geo[1]), 'tag':row['Tag']})

   return markers

@app.route('/')
def root():
   markers = get_latlon()
   setup=markers[0]  

   return render_template('index.html',markers=markers, setup=setup )

@app.route('/company')
def company():
   #todo: make the map take a coordinate
   markers = get_companies()
   setup={'lat':0, 'lon':0} 

   return render_template('companies.html',markers=markers, setup=setup )

if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)

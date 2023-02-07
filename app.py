from flask import Flask, render_template
import pandas as pd

app=Flask(__name__)

def open_file ():
   data = pd.read_csv('locations.txt')
   return data.iloc[:, [1,2]]

def get_latlon():
   '''
    Function to get the map data
   '''
   markers = []
   ll_data = open_file()

   for index, row in ll_data.iterrows():
      markers.append({'lat': float(row[0]), 'lon': float(row[1])})

   return markers

@app.route('/')
def root():
   #todo: make the map take a coordinate
   markers = get_latlon()
   setup=markers[0]
   #print(setup)   

   return render_template('index.html',markers=markers, setup=setup )

if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)

import os
from flask import Flask,redirect,url_for,render_template
import csv
from flask import request
app=Flask(__name__)

@app.route("/")
def home():
    results=[]
    with open('CSV/database.csv') as f: 
        mylist = [line.rstrip('\n') for line in f]
        reader = csv.DictReader(mylist)
        for row in reader:
            results.append(dict(row))

        return render_template('HomePage.html', results=results)

@app.route('/AboutUs')
def root():
        return render_template('AboutUs.html')

    
if __name__=="__main__":
     app.run(debug=True, port=80, host='0.0.0.0')
   # app.run()

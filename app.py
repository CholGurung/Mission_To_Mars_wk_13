from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from flask import send_from_directory 
import os
import scrape_mars
import pymongo

app = Flask(__name__)
print(app)
# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#conn = 'mongodb://localhost:27017'
#client =pymongo.MongoClient(conn)
#db = client.mars_db
#mars = db.mars_facts.find()

@app.route('/')
def index():
    mars_facts = mongo.db.mars_facts.find_one()
    #mars_facts = list(db.mars_facts.find())
    #mars = list(db.mars_facts.find())
    return render_template("index.html", mars_facts=mars_facts)
   
   
@app.route('/scrape')
def scrape():
    #mars = mongo.db.mars
    mars_facts = mongo.db.mars_facts
    mars_data = scrape_mars.scrape()
    #print("scrape data in app_py" + str(mars_facts))
    #mars_facts.update(
    #{},
    #mars_facts,
    #upsert=True
    #)
    
    #mycol = mydb["mars_facts"]
    #db.insert(mars_facts)
    mars_facts.update(
        {},
        mars_data,
        upsert = True

    )
    return redirect("/",code=302)

from flask import send_from_directory     

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == "__main__":
    app.run(debug=True)
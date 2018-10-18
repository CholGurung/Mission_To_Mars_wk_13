from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import pymongo
import scrape_mars


app = Flask(__name__)
print(app)
# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_facts

@app.route("/")
def index():
    #mars = mongo.db.mars.find_one()
    mars = list(db.mars_facts.find())
    return render_template("index.html", mars=mars)
   
   
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
    {},
    mars_data,
    upsert=True
    )
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run(debug=True)
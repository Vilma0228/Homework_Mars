# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo 
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
mongo = PyMongo(app)

# create mongo connection
client = pymongo.MongoClient()
db = client.mars_data_DB
mars_collection = db.mars_data_collection

@app.route("/")
def index():
    mars_data = mongo.db.listings.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
   #db.collection.remove({})
    mars_data = scrape_mars.scrape()
    hemi_dicts = scrape_mars.scrape()
    db.collection.insert_one(mars_data)
    db.collection.insert_one(hemi_dicts)

# Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo 
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
#conn = "mongodb://localhost:27017/db"
mongo = PyMongo(app)

# create mongo connection
#client = pymongo.MongoClient(conn)
#db = client.mars_data_db
#db.mars_data.drop()
# mars_collection = db.mars_data_collection


@app.route("/")
def index():
        mars_data = mongo.db.mars_data.find_one()
        print(mars_data)
        return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    #db.collection.remove({})
        mars = mongo.db.mars_data
        mars_data = scrape_mars.scrape()
        mars.update(
        {},
        mars_data,
        upsert=True
)
        return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
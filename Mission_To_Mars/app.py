#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create the app
app = Flask(__name__)

# establish the mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create a collection
mars_collection = mongo.db.mars

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_results = mars_collection.find_one()
    
    # pass those results to render_template
    return render_template("index.html", mars=mars_results)

@app.route("/scrape")
def scraper():
    # call scrape function in scrape_mars file. this scrapes and saves to mongo
    mars_data = scrape_mars.scrape()
    
    # update listings with the data or create and insert if the collection doesn't exist
    mars_collection.update_one({}, {"$set": mars_data}, upsert=True)
    
    # return a message to indicate success
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


#####################################################################################
# Dependencies and Setup
#####################################################################################
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import mars_scrape
import os

#####################################################################################
# Setup Flask app
#####################################################################################
app = Flask(__name__)

#####################################################################################
# Use flask_pymongo to set up mongo connection locally 
# The default port used by MongoDB is 27017
#####################################################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#####################################################################################
# Setup Flask routes
#####################################################################################

#--------------------------------------------------------------------------------
# Define the index route
#--------------------------------------------------------------------------------
@app.route("/")
def home():
    #----------------------------------------------------------------------------
    # Define DB, perform scraping so initial page has data displayed, update the 
    # data in the database, read the data from the database and send it to the 
    # template index.html page to be rendered.
    #----------------------------------------------------------------------------
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#--------------------------------------------------------------------------------
# Define /scrape route to be executedd when user hits the Scrape New Data button
#--------------------------------------------------------------------------------
@app.route("/scrape")
def scrape():
    #----------------------------------------------------------------------------
    # Since all scraping and page display is handled by the index route, redirect 
    # the user to the index page.
    #----------------------------------------------------------------------------
    return redirect("/", code=302)

#####################################################################################
if __name__ == "__main__": 
    app.run(debug= True)
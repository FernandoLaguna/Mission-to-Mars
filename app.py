
# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# use the scraping code, we will convert from Jupyter notebook to Python
import scraping

#Set the name for Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# tell Python how to connect to Mongo using PyMongo. Next, add the following lines
# our app will connect to Mongo using a URI. 
# mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script
   mars = mongo.db.mars.find_one()
   #tells Flask to return an HTML template using an index.html file, We'll create this file after we build the Flask routes. , 
   # moon=mars create a moon variable to use in index.html linkink it with mars = mongo.db.mars.find_one() 
   return render_template("index.html", moon=mars)

#defines the route that Flask will be using
@app.route("/scrape")
def scrape():
   # sign a new variable that points to our Mongo database
   mars = mongo.db.mars
    #create a new variable to hold the newly scraped data. Referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook
   mars_data = scraping.scrape_all()
   # first we'll need to add an empty JSON object with {}. Then, use the data we have stored in mars_data. upsert=True create a new document if doesn't already exist
   mars.update({}, mars_data, upsert=True)
   #navigate our page back to / where we can see the updated content.
   return redirect('/', code=302)

# code we need for Flask is to tell it to run
if __name__ == "__main__":
   app.run()


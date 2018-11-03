from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
#db.mars_info.drop()

# Set route

@app.route("/")
def index():
    mars_info = db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)

@app.route('/scrape')
def scrape():

    print("-----> Calling Scrape")

    mars_data = scrape_mars.scrape()

    print(mars_data)

    print("-----> Dropping mars data table form  db")   
    # Drops collection if available to remove duplicates
    db.mars_info.drop()

    print("-----> Inserting into db")

    db.mars_info.insert_one(mars_data)

    print("-----> Done - Inserting into db")

    return index()

if __name__ == "__main__":
    app.run(debug=True)

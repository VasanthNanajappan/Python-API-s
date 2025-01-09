import os
from flask import Flask
from flask import render_template
from flask import request
#request module allows us to easily handle any HTTP requests
from flask import redirect

from pymongo import MongoClient

################
#DB connection

MONGO_URI="mongodb://localhost:27017/"
client=MongoClient(MONGO_URI)

db=client['myCredDB']
collection=db['book_info']

#############

app=Flask(__name__)


@app.route("/",methods=["GET","POST"])

def home():
    # request.form -> it checks if someone submitted the form
    if request.method=="POST":
        title=request.form.get("title")
        if title:
            collection.insert_one({"title":title})
            return "Book added Successfully!"
    return render_template("home.html")

@app.route("/books",methods=["GET"])
def get_books():
    books=collection.find({})
    return render_template("books.html",books=books)

@app.route("/update",methods=["POST"])
def update():
    newtitle=request.form.get("newtitle")
    oldtitle=request.form.get("oldtitle")
    collection.update_one(
    {"title": oldtitle},  # Condition to match the book
    {"$set": {"title": newtitle}}  # Update operation
)
    return redirect("/books")

@app.route("/delete",methods=["POST"])
def delete():
    title=request.form.get("title")
    if title:
        collection.delete_one({"title":title})
        return redirect("/books")
    return "Error:Book not found"



if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)

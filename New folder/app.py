import base64
from flask import Flask, request, render_template, redirect,session
from pymongo import MongoClient
from flask_wtf import FlaskForm
import urllib.parse
from flask_wtf.csrf import CSRFProtect
import os
secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key 
csrf = CSRFProtect(app)
username = urllib.parse.quote_plus("Rutvik07")
password = urllib.parse.quote_plus("Rutvikrj@07")
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.txxteea.mongodb.net/')
db = client['input_output']
person_collection = db['Person']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = person_collection.find_one({"email": email})
        if user and user["password"] == password:
            user["image"] = base64.b64encode(user["image"]).decode('utf-8')
            user["_id"] = str(user["_id"])
            session['email'] =  user['email']
            return redirect("/user")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        address = request.form.get("address")
        image = request.files['image'].read()  # Reading image file data
        password = request.form.get("password")
        email = request.form.get("email")
        phone = request.form.get("phone")

        user_data = {
            "firstname": firstname,
            "address": address,
            "image": image,
            "email": email,
            "password": password,
            "phone": phone
        }
        person_collection.insert_one(user_data)
        return redirect("/login")
    return render_template("register.html")

@app.route('/user')
def user():
    email = session['email']
   
    user = person_collection.find_one({"email": email})
    id = str(user['_id'])
    image = base64.b64encode(user["image"]).decode('utf-8')
    firstname = user['firstname']
    address = user['address']
    email = user['email']
    phone = user['phone']
    if (firstname and address and image and email and id and phone):
        return render_template("user.html", firstname=firstname, address=address, image=image, email=email, phone=phone, id=id)
    else:
        return redirect("/login")

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")

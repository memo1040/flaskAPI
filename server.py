from flask import Flask, abort, render_template, request
from pymongo import cursor
from pymongo.uri_parser import parse_host
from mock_data import mock_data
from flask_cors import CORS
from config import db, json_parse
import json
from bson import ObjectId

app = Flask(__name__)
CORS(app) # allow anyone to call the server (**DANGER**)


coupon_codes = [
    {
        "code": "qwerty",
        "discount": 10
    }
]


me = {
    "name": "Guillermo",
    "last": "Monge",
    "age": 32,
    "hobbies": [],
    "email": "gmt1040@gmail.com",
    "address": {
        "street": "Delta",
        "city": "San Diego"
    }
}


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/test")
def simple_test():
    return "Hello there!"


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/about/email")
def email():
    return me["email"]

@app.route("/about/address")
def address():
    return me["address"]["street"] + ", " + me["address"]["city"]



###########################################
############## API Methods
###########################################


@app.route("/api/catalog", methods=["get"])
def get_catalog():
    #returns the catalog as JSON string
    catalog = []
    cursor = db.products.find({}) # find with no filters
    for prod in cursor:
        catalog.append(prod)

    print(len(catalog), "Records obtained from db")

    return json_parse(catalog) # error

@app.route("/api/catalog", methods=["post"])
def save_product():
    # get request payload (body)
    product = request.get_json()

    ## validate that title exists in the dict, if not abort(400)
    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title is required, and should contain at least 5 characters") # 400 = bad request

    ## validate that price exists and is greater than 0
    if not "price" in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should be a valid number")

    if product["price"] <= 0:
        return abort(400, "Price should be greater than 0")

    # save the product
    db.products.insert_one(product)

    # return the saved object
    return json_parse(product)

@app.route("/api/categories")
def get_categories():
    categories = []
    cursor = db.products.find({})
    for prod in cursor:
        if not prod["category"] in categories:
            categories.append(prod["category"])
    
    return json_parse(categories)


@app.route("/api/product/<id>")
def get_product(id):
    product = db.products.find_one({"_id": ObjectId(id)})
    if not product:
          return abort(404) # 404 = Not Found

    return json_parse(product)

    
@app.route("/api/catalog/<category>")
def get_by_category(category):
    cursor = db.products.find({"category": category})
    list = []
    for prod in cursor:
        list.append(prod)

    return json_parse(list)


@app.route("/api/cheapest")
def get_cheapest():
    cursor = db.products.find({})
    pivot = cursor[0]
    for prod in cursor: 
        if prod["price"] < pivot["price"]:
            pivot = prod

    return json_parse(pivot)


###########################################
############# Coupon Codes ################
###########################################

# POST to /api/couponCodes
@app.route("/api/couponCodes", methods=["post"])
def save_coupon():
    coupon = request.get_json()

    # validations
    if not "code" in coupon or len(coupon["code"]) < 5:
        return abort(400, "Code is required, and should contain at least 5 characters")

    # save
    db.couponCodes.insert_one(coupon)
    return json_parse(coupon)

# GET to /api/couponCodes
@app.route("/api/couponCodes", methods=["get"])
def get_coupons():
    coupon_codes = []
    cursor = db.couponCodes.find({})
    for prod in cursor:
        coupon_codes.append(prod)
    return json_parse(coupon_codes)


# get coupon by its code or 404 if not found
@app.route("/api/couponCodes/<code>")
def get_coupon_by_code(code):
    coupon = db.couponCodes.find_one({"code": code})
    if coupon is None:
        return abort(404, "Coupon code doesn't exist")
    return json_parse(coupon)


@app.route("/test/onetime/filldb")
def fill_db():
    # iterate the mock_data list
    for prod in mock_data:
        # save every object to db.products
        prod.pop("_id") # removes the id
        db.products.insert_one(prod) # stores

    return "Done!"

# start the server
# debug true will restart the server automatically
app.run(debug=True)
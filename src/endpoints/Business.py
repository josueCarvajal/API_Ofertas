from flask import Blueprint, jsonify, request
import db.FirebaseAdmin as firebase
from endpoints.User import addBusinessRef,deleteBusinessRef
business_endpoint = Blueprint('business_endpoint', __name__)

#Collection of the business
businessCollection = firebase.db.collection('business')

##### ROUTES #####

# Creates a new document entry in Business collection.
# business_id as document name
# @return String
@business_endpoint.route("/create", methods=['POST'])
def createBusiness():
    business_id = firebase.createCollection(businessCollection,request.json)
    user_id = request.json['user_id']
    addBusinessRef(user_id,business_id)
    return "Added successfully"

# Get a document by id
@business_endpoint.route("/get")
def getBusiness():
    business_id = request.json['business_id'] 
    return firebase.getDocument(businessCollection,business_id)

# Update a business by id
@business_endpoint.route("/update/<string:business_id>", methods=["POST"])
def updateBusiness(business_id):
    firebase.updateDocument(businessCollection,business_id,request.json)
    return "Business updated"

# Get the business owned by an user
@business_endpoint.route("/get/user")
def getBusinessByUser():
    user_id = request.json['user_id']
    businessList = firebase.getAllDocumentsByFilter(businessCollection,'user_id','==',user_id)
    return jsonify(businessList)

# Detele a business by id
@business_endpoint.route("/delete/", methods=['POST'])
def deleteBusiness():
    business_id = request.json['business_id']
    user_id = request.json['user_id']
    firebase.deleteDocument(businessCollection,business_id)
    deleteBusinessRef(user_id,business_id)
    return "Removed successfully"


##### METHODS #####

# Add a new post to a business by postid
def addPostRef(business_id,post_id):
    businessCollection.document(business_id).update({
        "posts": firebase.firestore.ArrayUnion([post_id])
    })

# Delete a post from business by postid
def deletePostRef(business_id,post_id):
    businessCollection.document(business_id).update({
        "posts": firebase.firestore.ArrayRemove([post_id])
    })

# Load the business info required by the post
def getBusinessById(business_id):
    return firebase.getDocument(businessCollection,business_id)
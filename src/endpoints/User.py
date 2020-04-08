from flask import Blueprint, jsonify, request
import db.FirebaseAdmin as firebase
user_endpoint = Blueprint('user_endpoint', __name__)

#Collection of the user
userCollection = firebase.db.collection('users')

# Creates a new document with the user id as document name
# @return String
@user_endpoint.route("/create", methods=['POST'])
def createUser():
    #here we do not know the document id
    userCollection.document(request.json['user_id']).set(request.json)
    return "User saved successfully"

# Get an user by id
# @return the user document as json
@user_endpoint.route("/get")
def getUser():
    user_id = request.json['user_id']
    return firebase.getDocument(userCollection,user_id)

# Update an existing user
@user_endpoint.route("/update", methods=['POST'])
def updateUser():
    user_id = request.json['user_id']
    firebase.updateDocument(userCollection,user_id,request.json)
    return "User updated successfully"


# Add a new business to a user by userid
def addBusinessRef(user_id,business_id):
    userCollection.document(user_id).update({
        "business": firebase.firestore.ArrayUnion([business_id])
    })

# Delete a business from an user by businessid
def deleteBusinessRef(user_id,business_id):
    userCollection.document(user_id).update({
        "business": firebase.firestore.ArrayRemove([business_id])
    })


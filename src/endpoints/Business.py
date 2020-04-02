from flask import Blueprint, jsonify, request
from db.FirebaseAdmin import db,firestore
from endpoints.User import addBusinessRef,deleteBusinessRef

business_endpoint = Blueprint('business_endpoint', __name__)

#Collection of the business
businessCollection = db.collection('business')


# Creates a new document entry in Business collection.
# business_id as document name
# @return String
@business_endpoint.route("/create", methods=['POST'])
def createBusiness():
    business_id = businessCollection.document().id
    businessCollection.document(business_id).set(request.json)
    user_id = request.json['user_id']
    #update the business at the user collection
    addBusinessRef(user_id,business_id)
    return "Added successfully"

@business_endpoint.route("/delete/", methods=['POST'])
def deleteBusiness():
    business_id = request.json['business_id']
    user_id = request.json['user_id']
    businessCollection.document(business_id).delete()
    deleteBusinessRef(user_id,business_id)
    return "Removed successfully"


@business_endpoint.route("/get")
def getBusiness():
    business_id = request.json['business_id']
    return businessCollection.document(business_id).get().to_dict()

@business_endpoint.route("/get/user")
def getBusinessByUser():
    user_id = request.json['user_id']
    businessByUser = businessCollection.where('user_id','==',user_id).stream()
    businessList = []
    for business in businessByUser:
        businessList.append(business.to_dict())
    return jsonify(businessList)

@business_endpoint.route("/update/<string:business_id>", methods=["POST"])
def updateBusiness(business_id):
    businessCollection.document(business_id).set(request.json)
    return "Business updated"


# Add a new post to a business by postid
def addPostRef(business_id,post_id):
    businessCollection.document(business_id).update({
        "posts": firestore.ArrayUnion([post_id])
    })

# Delete a post from business by postid
def deletePostRef(business_id,post_id):
    businessCollection.document(business_id).update({
        "posts": firestore.ArrayRemove([post_id])
    })
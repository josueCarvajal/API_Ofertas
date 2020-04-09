from flask import Blueprint, jsonify, request
import db.FirebaseAdmin as firebase
import calendar
import time
from endpoints.Business import addPostRef,deletePostRef,getBusinessById
post_endpoint = Blueprint('post_endpoint', __name__)

#Collection of the business
postCollection = firebase.db.collection('post')
#The number of posts retrieved by request
CHUNK_SIZE = 10

# Creates a new document entry in Business collection.
# business_id as document name
# @return String
@post_endpoint.route("/create", methods=['POST'])
def createPost():
    post_id = firebase.createCollection(postCollection,request.json)
    business_id = request.json["business_id"]
    addPostRef(business_id,post_id)
    return jsonify({"message": "Added successfully", "status": True, "id": post_id})

# Update an existing post
# @param String The post id
@post_endpoint.route("/update/<string:post_id>", methods=["POST"])
def updatePost(post_id):
    firebase.updateDocument(postCollection,post_id,request.json)
    return jsonify({"message": "Post updated successfully", "status": True})

# Delete a post by id
@post_endpoint.route("/delete", methods=['POST'])
def deletePost():
    business_id = request.json['business_id']
    post_id = request.json['post_id']
    firebase.deleteDocument(postCollection,post_id)
    deletePostRef(business_id,post_id)
    return jsonify({"message": "Post Removed successfully", "status": True})

#get a post by id
@post_endpoint.route("/get")
def getPost():
    postDetails = []
    post_id = request.json['post_id']
    businessInfo = getBusinessById(request.json['business_id'])
    postInfo = firebase.getDocument(postCollection,post_id)
    postDetails.append(businessInfo)
    postDetails.append(postInfo)
    return jsonify(postDetails)

# get the posts owned by a business id
@post_endpoint.route("/get/business")
def getPostsByBusiness():
    business_id = request.json['business_id']
    postList = firebase.getAllDocumentsByFilter(postCollection,'business_id','==',business_id)
    return jsonify(postList)

# Get the first chunk of posts. Limited by the CHUNK_SIZE (10 Default)
@post_endpoint.route("/get/chunk")
def getFirstChunkOfPosts():
    retrievedDocs = []
    systemDate = calendar.timegm(time.gmtime())
    docs = postCollection.where('expiry_time','>=',str(systemDate)).order_by('expiry_time').limit(CHUNK_SIZE).stream()
    for doc in docs:
        retrievedDocs.append(doc.to_dict())
    return jsonify(retrievedDocs)

# Get the next chunk of posts.
# Requires the last retrieved chunk info
@post_endpoint.route("/get/next/chunk", methods = ['POST'])
def getNextChunkOfPosts():
    retrievedDocs = []
    lastPost = request.json["expiry_time"]
    systemDate = calendar.timegm(time.gmtime())
    docs = postCollection.where('expiry_time','>=',str(systemDate)).order_by('expiry_time').start_after({'expiry_time': lastPost}).limit(CHUNK_SIZE).stream()
    for doc in docs:
        retrievedDocs.append(doc.to_dict())
    return jsonify(retrievedDocs)
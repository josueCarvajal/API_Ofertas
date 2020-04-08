from flask import Blueprint, jsonify, request
import db.FirebaseAdmin as firebase
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
    return "Added successfully"

# Update an existing post
# @param String The post id
@post_endpoint.route("/update/<string:post_id>", methods=["POST"])
def updatePost(post_id):
    firebase.updateDocument(postCollection,post_id,request.json)
    return "Post updated"

# Delete a post by id
@post_endpoint.route("/delete", methods=['POST'])
def deletePost():
    business_id = request.json['business_id']
    post_id = request.json['post_id']
    firebase.deleteDocument(postCollection,post_id)
    deletePostRef(business_id,post_id)
    return "Removed successfully"

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
    docs = postCollection.order_by('created_at').limit(CHUNK_SIZE).stream()
    for doc in docs:
        retrievedDocs.append(doc.to_dict())
    return jsonify(retrievedDocs)

# Get the next chunk of posts.
# Requires the last retrieved chunk info
@post_endpoint.route("/get/next/chunk", methods = ['POST'])
def getNextChunkOfPosts():
    retrievedDocs = []
    lastPost = request.json["created_at"]
    docs = postCollection.order_by('created_at').start_after({'created_at': lastPost}).limit(CHUNK_SIZE).stream()
    for doc in docs:
        retrievedDocs.append(doc.to_dict())
    return jsonify(retrievedDocs)



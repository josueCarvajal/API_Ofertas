from flask import Blueprint, jsonify, request
from db.FirebaseAdmin import db
from endpoints.Business import addPostRef,deletePostRef,getBusinessById
post_endpoint = Blueprint('post_endpoint', __name__)

#Collection of the business
postCollection = db.collection('post')

#The number of posts retrieved by request
CHUNK_SIZE = 10
# Creates a new document entry in Business collection.
# business_id as document name
# @return String
@post_endpoint.route("/create", methods=['POST'])
def createPost():
    post_id = postCollection.document().id
    postCollection.document(post_id).set(request.json)
    business_id = request.json["business_id"]
    #update the business at the user collection
    addPostRef(business_id,post_id)
    return "Added successfully"


# Update an existing post
# @param String The post id
@post_endpoint.route("/update/<string:post_id>", methods=["POST"])
def updatePost(post_id):
    postCollection.document(post_id).set(request.json)
    return "Post updated"

# Delete a post by id
@post_endpoint.route("/delete", methods=['POST'])
def deletePost():
    business_id = request.json['business_id']
    post_id = request.json['post_id']
    postCollection.document(post_id).delete()
    deletePostRef(business_id,post_id)
    return "Removed successfully"

#get a post by id
@post_endpoint.route("/get")
def getPost():
    postDetails = []
    post_id = request.json['post_id']
    businessInfo = getBusinessById(request.json['business_id'])
    postInfo = postCollection.document(post_id).get().to_dict()
    postDetails.append(businessInfo)
    postDetails.append(postInfo)
    return jsonify(postDetails)

# get the posts owned by a business id
@post_endpoint.route("/get/business")
def getPostsByBusiness():
    business_id = request.json['business_id']
    postsByBusiness = postCollection.where('business_id','==',business_id).stream()
    postList = []
    for post in postsByBusiness:
        postList.append(post.to_dict())
    return jsonify(postList)


@post_endpoint.route("/get/chunk")
def getFirstChunkOfPosts():
    retrievedDocs = []
    docs = postCollection.order_by('created_at').limit(CHUNK_SIZE).stream()
    for doc in docs:
        retrievedDocs.append(doc.to_dict())
    return jsonify(retrievedDocs)


@post_endpoint.route("/get/next/chunk", methods = ['POST'])
def getNextChunkOfPosts():
    retrievedDocs = []
    lastPost = request.json["created_at"]
    docs = postCollection.order_by('created_at').start_after({'created_at': lastPost}).limit(CHUNK_SIZE).stream()
    for doc in docs:
        retrievedDocs.append(doc.to_dict())
    return jsonify(retrievedDocs)



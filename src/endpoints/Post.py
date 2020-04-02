from flask import Blueprint, jsonify, request
from db.FirebaseAdmin import db
from endpoints.Business import addPostRef,deletePostRef
post_endpoint = Blueprint('post_endpoint', __name__)

#Collection of the business
postCollection = db.collection('post')


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
    post_id = request.json['post_id']
    return postCollection.document(post_id).get().to_dict()

#get all the posts available
@post_endpoint.route("/get/all")
def getAllPosts():
    posts = postCollection.stream()
    allPosts = []
    for post in posts:
        allPosts.append(post.to_dict())
    return jsonify(allPosts)

# get the posts owned by a business id
@post_endpoint.route("/get/business")
def getPostsByBusiness():
    business_id = request.json['business_id']
    postsByBusiness = postCollection.where('business_id','==',business_id).stream()
    postList = []
    for post in postsByBusiness:
        postList.append(post.to_dict())
    return jsonify(postList)
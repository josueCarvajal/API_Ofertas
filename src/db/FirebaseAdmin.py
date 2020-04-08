import firebase_admin
from firebase_admin import credentials,firestore,exceptions

cred = credentials.Certificate("ServiceAccountKey.json path here")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Creates a new collection
# @param collection the collection name (post,users,business)
# @param request The json request
def createCollection(collection, request):
    entry_id = collection.document().id
    collection.document(entry_id).set(request)
    return entry_id

# Get a single document by id
# @param collection the collection name (post,users,business)
# @param document_id The id of the document desired
def getDocument(collection,document_id):
    return collection.document(document_id).get().to_dict()

# Get all the documents that match to a filter
# @param collection the collection name (post,users,business)
# @param document_field The field_name of the document desired to filter
# @param operator The operator that the filter will apply i.e ==
# @param value The value to filter
def getAllDocumentsByFilter(collection,document_field,operator,value):
    documents = collection.where(document_field,operator,value).stream()
    documentList = []
    for document in documents:
        documentList.append(document.to_dict())
    return documentList

# Update a single document by id
# @param collection the collection name (psot,user,business)
# @param document_id The id of the document desired to update
# @param request The updated values
def updateDocument(collection,document_id,request):
    collection.document(document_id).set(request)
    return "OK"

# Delete a single document by id
# @param collection the collection name (psot,user,business)
# @param document_id The id of the document desired to delete
def deleteDocument(collection,document_id):
    collection.document(document_id).delete()
    return "OK"

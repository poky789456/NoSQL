from pymongo import MongoClient
import pymongo

client = MongoClient('mongodb://localhost:27017/')

db = client.mydb
collection = db.mycollection

# Create (insert) : un seul document
# document = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
# result = collection.insert_one(document)
# print("Inserted document ID:", result.inserted_id)

# Plusieurs documents
# documents2 = [
#     {"name": "Alice", "email": "alice@example.com", "age": 25},
#     {"name": "Bob", "email": "bob@example.com", "age": 35}
# ]
# result = collection.insert_many(documents2)
# print("Inserted document IDs:", result.inserted_ids)

# Read (query) : un seul document

# query = {"name": "John Doe"}

# document2 = collection.find_one(query)

# Plusieurs documents
# query = {"age": {"$gt": 25}}
# documents = collection.find(query)

# for doc in documents:
#     print(doc)

# Update : Un seul document

# query = {"name": "John Doe"}
# update = {"$set": {"age": 31}}
# result = collection.update_one(query, update)
# print("Modified document count:", result.modified_count)

# Update : plusieurs documents

# query = {"age": {"$gt": 25}}
# update = {"$inc": {"age": 1}}
# result = collection.update_many(query, update)
# print("Modified document count:", result.modified_count)


# Delete : un seul document

# query = {"name": "John Doe"}
# result = collection.delete_one(query)
# print("Deleted document count:", result.deleted_count)

# Delete : plusieurs documents
# query = {"age": {"$gt": 25}}
# result = collection.delete_many(query)
# print("Deleted document count:", result.deleted_count)

# Opérateurs logiques

# query = {
#     "$and": [
#         {"age": {"$gt": 25}},
#         {"email": {"$regex": "@example\.com$"}}
#     ]
# }
# documents = collection.find(query)

# for doc in documents:
#     print(doc)


# Projection

# query = {"age": {"$gt": 25}}
# projection = {"_id": 0, "name": 1, "email": 1}
# documents = collection.find(query, projection)

# for doc in documents:
#     print(doc)

# Tri 

query = {"age": {"$gt": 25}}
documents = collection.find(query).sort("name", pymongo.ASCENDING)

for doc in documents:
    print(doc)

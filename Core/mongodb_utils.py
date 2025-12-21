"""
MongoDB Helper Functions
Provides utility functions for MongoDB operations
"""

from bson import ObjectId
from datetime import datetime

def get_db():
    """Get MongoDB database instance"""
    from django.conf import settings
    if hasattr(settings, 'mongodb_db') and settings.mongodb_db is not None:
        return settings.mongodb_db
    else:
        # Fallback: create connection if not exists
        from pymongo import MongoClient
        from decouple import config
        
        MONGODB_URI = config('MONGODB_URI')
        MONGODB_DB_NAME = config('MONGODB_DB_NAME', default='dogustansosyalDB')
        
        # SSL sertifika doğrulamasını devre dışı bırak (development için)
        mongodb_client = MongoClient(MONGODB_URI, tlsAllowInvalidCertificates=True)
        return mongodb_client[MONGODB_DB_NAME]

def serialize_mongo_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    if '_id' in doc:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return doc

def serialize_mongo_docs(docs):
    """Convert list of MongoDB documents to JSON-serializable list"""
    return [serialize_mongo_doc(doc) for doc in docs]

def get_object_id(id_str):
    """Convert string ID to ObjectId"""
    try:
        return ObjectId(id_str)
    except:
        return None

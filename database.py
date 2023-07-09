import pymongo
from settings import USERNAME, PORT, PASSWORD, HOSTNAME, DATABASE_NAME
from datetime import datetime
from abc import ABC, abstractmethod


class DbClient:
    def __init__(self, username, password, hostname, port):
        self.dblink = 'mongodb://' + username + ':' + password + '@' + hostname + ':' + port
        self.client = pymongo.MongoClient(self.dblink)

    def get_client(self):
        return self.client

    def get_database(self, database_name):
        return self.client[database_name]


class Model:
    def __init__(self):
        db_client = DbClient(USERNAME, PASSWORD, HOSTNAME, PORT)
        db = db_client.get_database(DATABASE_NAME)
        self.db = db
        self.collection = self.create_table()

    def create_table(self):
        return self.db[self.__class__.__name__]

    def add_document(self, document):
        self.collection.insert_one(document)

    def add_documents(self, documents):
        self.collection.insert_many(documents)

    def delete_document(self, _id=None, **kwargs):
        if _id:
            self.collection.delete_one({"_id": _id})
        else:
            self.collection.delete_one(kwargs)

    def delete_documents(self, **kwargs):
        self.collection.delete_many(kwargs)

    def get_documents(self, _id=None, **kwargs):
        if _id:
            return self.collection.find({"_id": _id})
        else:
            return self.collection.find(kwargs)

    def update_document(self, identifier, update):
        self.collection.update_one(identifier, {"$set": update})

    def update_documents(self, identifier, update):
        self.collection.update_many(identifier, {"$set": update})


class Datasets(Model):
    def __init__(self):
        super().__init__()

    def add_image_to_dataset(self, image, dataset_name, filename):
        self.add_document({"image": image, "dataset_name": dataset_name, "filename": filename})

    def add_images_to_dataset(self, images):
        self.add_documents(images)

    def delete_dataset(self, dataset_name):
        self.delete_documents(dataset_name=dataset_name)

    def update_dataset_name(self, dataset_name, new_dataset_name):
        self.update_documents({"dataset_name": dataset_name}, {"dataset_name": new_dataset_name})

    def change_image_dataset(self, _id, new_dataset_name):
        self.update_document({"_id": _id}, {"dataset_name": new_dataset_name})

    def get_dataset(self, dataset_name, count=None, idx=0, max_count=None):
        if count:
            if max_count:
                if (idx+1)*count > max_count:
                    return self.get_documents(dataset_name=dataset_name)[idx * count:max_count]
            return self.get_documents(dataset_name=dataset_name)[idx*count:(idx+1)*count]
        return self.get_documents(dataset_name=dataset_name)

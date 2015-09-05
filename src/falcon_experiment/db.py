#!/usr/bin/env python
# -*- coding: utf-8 -*-
from riak import RiakClient

db_client = RiakClient(protocol='pbc', host='127.0.0.1', http_port=8087)


def get(bucket_name, key):
    bucket = db_client.bucket(bucket_name)
    riakobject = bucket.get(key)
    if not riakobject.exists:
        raise KeyError('Object does not exist')

    return riakobject.key, riakobject.data


def create(bucket_name, dict_):
    bucket = db_client.bucket(bucket_name)
    riakobject = bucket.new(data=dict_)
    riakobject.store()
    return riakobject.key


def delete(bucket_name, key):
    bucket = db_client.bucket(bucket_name)
    riakobject = bucket.get(key)
    if not riakobject.exists:
        raise KeyError('Object does not exist')

    riakobject.delete()


def delete_all():
    for bucket in db_client.get_buckets():
        for key in bucket.get_keys():
            robj = bucket.get(key)
            robj.delete()


# class Storage(object):
#     _db = {}

#     def get(self, key):
#         return self._db[key]

#     def set(self, key, value):
#         self._db[key] = value

#     def delete(self, key):
#         del self._db[key]

#     def clear(self):
#         self._db = {}

#     def all(self):
#         return self._db

# db = Storage()
# db.set(
#     'Alice', {
#         'name': 'Alice',
#         'email': 'alice@example.com',
#         'created_at': 'time'
#     }
# )
# db.set(
#     'Bob', {
#         'name': 'Bob',
#         'email': 'bob@example.com',
#         'created_at': 'time'
#     }
# )

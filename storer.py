# -*- coding: utf-8 -*-
__author__ = 'CubexX'

import shelve


class Storer:
    def __init__(self, filename):
        self.filename = filename

    def store(self, key, obj):
        db = shelve.open(self.filename)
        db[key] = obj
        db.close()

    def restore(self, key):
        db = shelve.open(self.filename)
        if key in db:
            obj = db[key]
        else:
            obj = None
        db.close()
        return obj

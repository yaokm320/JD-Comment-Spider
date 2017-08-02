# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from jingdong import settings

class JingdongPipeline(object):

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['jingdong']
        self.collection = db["jingdong_cup"]

    def process_item(self, item, spider):
        content = dict(item)
        self.collection.insert_one(content)
        return "OK!"

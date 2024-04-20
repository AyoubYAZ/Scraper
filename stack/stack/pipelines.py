# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        connection=pymongo.MongoClient(settings['MONGODB_SERVER'],settings['MONGODB_PORT'])
        db=connection[settings['MONGODB_DB']]
        self.connection=db[settings['MONGODB_COLLECTION']]
    def  process_item(self, item, spider) :
        valid=True
        for data in item :
            if not data:
                valid=False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.connection.insert(dict(item))
            log.msg("question added to mongodb database!",level=log.DEBUG,spider=spider)
        return item 

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .db_mapping import *


class EventbritePipeline:
    def open_spider(self,spider):
        db.connect()
        if not Eventbrite.table_exists():
            Eventbrite.create_table()

    def process_item(self, item, spider):
        Eventbrite.insert(item).on_conflict('replace').execute()
        db.commit()
        return item






    
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

class JsonWriterPipeline(object):

    def __init__(self):
        #self.file = open('items.txt', 'w')
        pass
    def process_item(self, item, spider):
		#line = json.dumps(dict(item)) + "\n"
		#self.file.write(line)
		with open('items.txt','a') as f:
			number = 0
			f.write('{0}	{1}	{2}\n'.format(item['letter'],item['title'],item['text']))


		return item

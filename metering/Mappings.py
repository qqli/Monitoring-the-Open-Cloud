#!/usr/bin/env python

class Mappings(object):

#	from pymongo import MongoClient
#	client = MongoClient('mongodb://10.13.37.91:27017/')
#	db = client.ceilometer
	def __init__(self,db):
		self.db = db
# This function returns a mapping of each vm with host machine
# for each project
	def get_mappings(self):
		self.print_data()
		resources = self.db.meter.find({"resource_metadata.event_type":{'$regex':'compute'}},{"resource_metadata.event_type":1,"resource_metadata.host":1,'resource_id':1,'timestamp':1})	
		aggregates = self.db.meter.aggregate([
			{'$match':{'resource_metadata.event_type':{'$regex':'compute'}}},
			{'$sort':{'timestamp':1}},
			{'$group':{
				'_id':'$resource_id',
				'timestamp':{'$last':'$timestamp'},
				'event_type':{'$last':'$resource_metadata.event_type'},
				'host':{'$last':'$resource_metadata.host'},
				'project_id':{'$last':'$project_id'}
				}},
			{'$group':{
				'_id':'$project_id',
				'instance':{'$push':{'resource_id':'$_id','timestamp':'$timestamp','event_type':'$event_type','host':'$host'}}
			}}])	
		#print type(aggregates)
		if(aggregates['ok']):
			for item in aggregates['result']:
				print item,'\n'

	def print_data(self):
		print "------------------------------------"
		print "Mappings for all projects\n\t_id represents project_id"
		print "\tinstance field contains all instances\n\tresource_id represents VM's id\n\n"



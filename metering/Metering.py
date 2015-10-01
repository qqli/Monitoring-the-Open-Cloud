#!/usr/bin/env python
from datetime import datetime 
import Measurements

import json
import pprint
class Metering(object):
	
	def __init__(self,db):
		self.db = db
		self.dict = {}

	def get_instance(self):
		resource = self.db.resource.aggregate([
			{'$match':{'meter.counter_name':'instance'}},
			{'$project':{'project_id':1,'first_sample_timestamp':1,'last_sample_timestamp':1,'metadata.name':1,'metadata.vcpus':1,'metadata.memory_mb':1,'metadata.instance_type':1,'metadata.disk_gb':1,'metadata.root_gb':1}},
			{'$group':{
				'_id':'$project_id',
				'instance':{'$push':{'name':'$metadata.name'}}
			}}
		])	
		if(resource['ok']):
			for item in resource['result']:
				print item,'\n'


	def get_instance_allocation(self,start,end):
		
		resource_metadata = self.data_set()
		resource = self.db.meter.aggregate(
		[{'$match':{'$and':[
			{'recorded_at':{'$gte':start}},
			{'recorded_at':{'$lt':end}}]}},
		{'$match':{'counter_name':'instance'}},
		{'$group':{
			'_id':'$resource_id',
			'resource_metadata':resource_metadata,
			'project_id':{'$last':'$project_id'}
		}},
		{'$group':{
			'_id':'$project_id',
			'instance':{'$push':{'resource_id':'$_id','resource_metadata':'$resource_metadata'}}
		}}])
		if(resource['ok']):
			for item in resource['result']:
				print item,'\n'


	def data_set(self):
		resource = {'$last':{
			'instance_type':'$resource_metadata.instance_type',
			'name':'$resource_metadata.name',
			'vcpus':'$resource_metadata.vcpus',
			'memory_mb':'$resource_metadata.memory_mb',
			'disk_gb':'$resource_metadata.root_gb'
			}}
		status = {'$push':{
			'recorded_at':'$recorded_at',
			'status':'$resource_metadata.status'
			}}
		existance = {'$last':{
			'deleted_at':'$resource_metadata.deleted_at',
			'created_at':'$resource_metadata.created_at'
			}}
		event_type = {'$last':{
			'recorded_at':'$recorded_at',
			'event_type':'$resource_metadata.event_type'
			}}
		audit_period = {'$push':{
			'audit_period_beginning':'resource_metadata.audit_period_beginning',
			'audit_period_ending':'resource_metadata.audit_period_ending',
			'event_type':'resource_metadata.event_type'	
			}}
		return resource,status,existance,event_type,audit_period
	
	## This function takes in the start time, the end time and a meter from Measurements.compute()
	# Process it and returns a dictionary of project_id and instance for each project. 
	# 'instance' is a list which stores resource_id, counter_name and usage for each of the instance.
	def single_metering(self,start,end,meter):
		self.resource_list = []
		resource_metadata,status,existance,event_type,audit_period = self.data_set()
		resource = self.db.meter.aggregate(
		[{'$match':{'$and':[
			{'recorded_at':{'$gte':start}},
			{'recorded_at':{'$lt':end}}]}},
		{'$match':{'counter_name':meter}},
                {'$group':{
                    '_id':'$resource_id',
                    'resource_metadata':resource_metadata,
                    'project_id':{'$last':'$project_id'},
		    'first_sample':{'$first':'$counter_volume'},
		    'last_sample':{'$last':'$counter_volume'},
		    'counter_name':{'$last':'$counter_name'}
                }},
		{'$group':{
			'_id':'$project_id',
			'instance':{'$push':{'resource_id':'$_id','first_sample':'$first_sample','last_sample':'$last_sample','counter_name':'$counter_name'}}
			}}
		])
		if(resource['ok']):
			for item in resource['result']:
				for index,instance in enumerate(item['instance']):
					first_sample = item['instance'][index]['first_sample']
					last_sample = item['instance'][index]['last_sample']
					usage = last_sample - first_sample
					item['instance'][index]['usage']=usage
			self.resource_list.append(item)		
		return self.resource_list

	def instance_existance(self,start,end):
		resource_metadata,status,existance,event_type,audit_period = self.data_set()
		resource = self.db.meter.aggregate(
		[{'$match':{'$and':[
			{'recorded_at':{'$gte':start}},
			{'recorded_at':{'$lt':end}}]}},
		{'$match':{'counter_name':'instance'}},
                {'$group':{
                    '_id':'$resource_id',
                    'resource_metadata':resource_metadata,
                    'project_id':{'$last':'$project_id'},
                    'status':status,
                    'existance':existance,
		'event_type':event_type
                }}
		])
		if(resource['ok']):
			for item in resource['result']:
				print item,'\n'


	def meter_Cumulative(self,start,end):
		print '---------------------------------------'
		self.dict = Measurements.compute()
		meter_list = []
		self.project_list = []
		meter_params=['counter_name','first_sample','last_sample','usage']
		#self.project_dict ={'project_id':'','instance':[]} 
		for key in self.dict:
			if (self.dict[key]=='Cumulative'):
				meter_list.append(key)
				metering_result = self.single_metering(start,end,key)
				if (self.project_list == []):
					self.project_list = self.form_list(metering_result)
				else:
					self.project_list = self.append_list(metering_result,self.project_list)
		print self.project_list	
		self.project_list = self.sort_all_instances(self.project_list)	
		#print self.project_list


	def form_dict(self,item):
		meter_params=['counter_name','first_sample','last_sample','usage']
		project_dict = {'project_id':'','instance':[]}
			#print project_dict.has_key('project_id')
			#if (project_dict.has_key('project_id')==False):
		project_dict['project_id'] = item['_id']
		for index,value in enumerate(item['instance']):
			temp_dict = {'resource_id':'','meter':[]}
			temp_dict['resource_id'] = item['instance'][index]['resource_id']
			temp_dict2 = {}
			for param in meter_params:
				temp_dict2[param] = item['instance'][index][param]
			temp_dict['meter'].append(temp_dict2)
			project_dict['instance'].append(temp_dict)	
			#project_dict['instance'].append(item['instance'][index]['resource_id'])
		return project_dict

	def append_dict(self,item):
		meter_params=['counter_name','first_sample','last_sample','usage']
		for index,value in enumerate(item['instance']):
			temp_dict = {'resource_id':'','meter':[]}
			temp_dict['resource_id'] = item['instance'][index]['resource_id']
			temp_dict2 = {}
			for param in meter_params:
				temp_dict2[param] = item['instance'][index][param]
			temp_dict['meter'].append(temp_dict2)
			#project_dict['instance'].append(item['instance'][index]['resource_id'])
		return temp_dict
		
			
	def form_list(self,metering_result):
		project_list = []
		for item in metering_result:
			project_list.append(self.form_dict(item))
		return project_list
	def append_list(self,metering_result,project_list):
		for item in metering_result:
			for index,value in enumerate(project_list):
				if(item['_id']==project_list[index]['project_id']):
					project_list[index]['instance'].append(self.append_dict(item))
					continue
				project_list.append(self.form_dict(item))
			return project_list	
	def sort_instance(self,index,project_list):
		instances = project_list[index]['instance']
		instance_list = []
		for index1,instance in enumerate(instances):
			meters_list = []
			meter = instances[index1]['meter']
			resource_id = instances[index1]['resource_id']
			temp = {'resource_id':'','meters_list':[]}
			#if(instance_list==[]):
			#	meters_list.append(meter)
			#	temp['resource_id'] = resource_id
			#	temp['meters_list'] = meters_list
			#	instance_list.append(temp)
			for value in instance_list:
				print value
				#if(resource_id == value['resource_id']):
					#print value['resource_id']
					#print value['meters_list']
				#	meters_list = value['meters_list']
				#	meters_list.append(meter)
					#print meters_list
				#	temp['resource_id']=resource_id
				#	temp['meters_list'] = meters_list
				#	instance_list.append(temp)	
				#	continue
			meters_list.append(meter)
			temp['resource_id'] = resource_id
			temp['meters_list'] = meters_list
			instance_list.append(temp)
		print instance_list
		return instance_list

	def sort_all_instances(self,project_list):
		for index,project in enumerate(project_list):
			instance_list = self.sort_instance(index,project_list)
			project['instance'] = instance_list
		return project_list

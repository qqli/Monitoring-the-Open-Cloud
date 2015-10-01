
from datetime import datetime 
import json
import pprint

class TimeRange(object):
	def __init__(self,startMonth=None,endMonth=None,startDay=None,endDay=None,startHour=None,endHour=None):
		time = datetime.now()
		self.dict = {
			'startMonth':time.month,
			'startDay':time.day,
			'startHour':00,
			'endMonth':time.month,
			'endDay':time.day,
			'endHour':time.hour,
			'year':time.year}
		self.startMonth = startMonth
		self.endMonth = endMonth
		self.startDay = startDay
		self.endDay = endDay
		self.startHour = startHour
		self.endHour = endHour

	def get_timeRange(self):
		if(self.startMonth!=None):self.dict['startMonth']= self.startMonth
		if(self.endMonth!=None):self.dict['endMonth']= self.endMonth
		if(self.startDay!=None):self.dict['startDay'] = self.startDay
		if(self.endDay!=None):self.dict['endDay'] = self.endDay
		if(self.startHour!=None):self.dict['startHour'] = self.startHour
		if(self.endHour!=None):self.dict['endHour'] = self.endHour
		
		self.start = datetime(self.dict['year'],self.dict['startMonth'],self.dict['startDay'],self.dict['startHour'],00,00,000000)
		self.end = datetime(self.dict['year'],self.dict['endMonth'],self.dict['endDay'],self.dict['endHour'],00,00,000000)
		return self.start,self.end

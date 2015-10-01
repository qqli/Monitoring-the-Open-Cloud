#!/usr/bin/env python

from Mappings import *
from Metering import *
from Project import *
from TimeRange import *

def main():
#	print_data()
	from pymongo import MongoClient
	client = MongoClient('mongodb://10.13.37.91:27017/')
	db = client.ceilometer
	#adminData = Mappings(db)
	#adminData.get_mappings()
	timeRange = TimeRange(8,8,10,15,00,00)
	start,end = timeRange.get_timeRange()
	meterData = Metering(db)
	#meterData.get_instance_allocation(start,end)
	#project = Project(db)
	#project.update_collection()
	meterData.meter_Cumulative(start,end)
def print_data():
          print "------------------------------------"
          print "Mappings for all projects\n\t_id represents project_id"
          print "\tinstance field contains all instances\n\tresource_id represents VM's id\n\n"


if __name__ == "__main__":
	main()

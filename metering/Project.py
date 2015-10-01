

class Project(object):
	def __init__(self,db):
		self.db = db

	def update_collection(self):
		self.db.resource.aggregate([
			{'$group':{'_id':'$project_id'}},
			{'$out':'project'}])
		print "successfully update project collection"
		

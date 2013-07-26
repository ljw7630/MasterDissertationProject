from rdf_generator import RDFGenerator as RG
from html_parser import PublicProfileParser as ProfileParser
from os import listdir
from os.path import join
from utils import Utils
import glob
import sys
from profile_cleaner import ProfileCleaner as Cleaner
from socket_handler import DegreeSocketHandler
from db_helper import DBHelper
import traceback

## fix db scripts:

# import os
# from db_helper import DBHelper
#
# res = DBHelper.getNotRDFedFileName(limit=10000)
#
# for f in res:
# 	if os.path.exists('user_raw/'+f) or os.path.exists('company_raw/'+f):
# 		print f
# 		DBHelper.dataSetExists(f, 1)
#
##############################################################################
#
#
# res = os.listdir('user_raw')
#
# for f in res:
# 	print f
# 	DBHelper.dataSetExists(f, 1)
#
##############################################################################
#
# import os
# from db_helper import DBHelper
#
# res = DBHelper.getNotRDFedFileName(limit=10000)
#
# for f in res:
# 	if (not os.path.exists('user_raw/'+f)) and (not os.path.exists('company_raw/'+f)):
# 		print f
# 		DBHelper.deleteDataInDB(f)
##############################################################################
# from db_helper import DBHelper
# res = DBHelper.getFileNames(limit=10000)
# for f in res:
# 	print f
# 	DBHelper.dataSetRDF(f, rdf=0)


def cleanProfile():
	path = 'user_raw'
	for f in listdir(path):
		file_path = join(path, f)
		cleaner = Cleaner(file_path)
		cleaner.saveToFile(file_path)


def getPublicProfiles(limit=1000):
	path = 'user_raw'
	profile_paths = []

	for f in DBHelper.getNotRDFedFileName(limit):
		file_path = join(path, f)
		profile_paths.append(file_path)
	# 	parser = ProfileParser(file_path)
	# 	profile = parser.parseHtml()
	# 	profiles.append(profile)
	# return profiles
	return profile_paths


def printList(arr):
	for item in arr:
		print item


def validateDegreeEngine():
	sh = DegreeSocketHandler()
	sh.send_query_command()
	profiles = getPublicProfiles()

	for profile in profiles:
		for education in profile.education_list:
			if 'degree' in education:
				print sh.send_query(education['degree'])
				print '\n'

	sh.close()


def run(num):
	rg = RG()
	profile_paths = getPublicProfiles(limit=num)
	try:
		for path in profile_paths:
			parser = ProfileParser(path)
			profile = parser.parseHtml()
			print profile.extra_profile_list
			Utils.putExtraProfilesIntoDB(profile.extra_profile_list)
			rg.add(profile)
			DBHelper.dataSetRDF(profile.file_name, rdf=1)
	except Exception:
		traceback.print_exc()
		rg.save(format='xml')
		rg.close()
		DBHelper.commitAndClose()
	else:
		rg.save(format='xml')
		rg.close()
		DBHelper.commitAndClose()


def main(argv):
	num = 100
	if len(argv) == 1:
		num = 100
	else:
		num = int(argv[1])
	run(num)

if __name__ == '__main__':
	main(sys.argv)
from rdf_generator import RDFGenerator as RG
from html_parser import PublicProfileParser as ProfileParser
from os import listdir
from os.path import join
from utils import Utils
import glob
from profile_cleaner import ProfileCleaner as Cleaner
from socket_handler import DegreeSocketHandler


def cleanProfile():
	path = 'user_raw'
	for f in listdir(path):
		file_path = join(path, f)
		cleaner = Cleaner(file_path)
		cleaner.saveToFile(file_path)


def getPublicProfiles():
	path = 'user_raw'
	profiles = []

	for f in listdir(path):
		file_path = join(path, f)
		parser = ProfileParser(file_path)
		profile = parser.parseHtml()
		profiles.append(profile)
	return profiles


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


def main():
	# validateDegreeEngine()
	# cleanProfile()
	profiles = getPublicProfiles()
	# Utils.persistentPublicProfiles(profiles)
	rg = RG()

	for profile in profiles:
		rg.add(profile)

	rg.save(format='xml')

if __name__ == '__main__':
	main()
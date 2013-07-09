from rdf_generator import RDFGenerator as RG
from html_parser import PublicProfileParser as ProfileParser
from os import listdir
from os.path import join
from utils import Utils


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


def main():
	profiles = getPublicProfiles()
	Utils.persistentPublicProfiles(profiles)
	rg = RG()

	for profile in profiles:
		rg.add(profile)

	rg.save(format='xml')


if __name__ == '__main__':
	main()
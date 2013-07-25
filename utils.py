import os
import sqlite3
from db_helper import DBHelper
import html_parser
import pickle
import json
import urllib2
import logging
import sys
import traceback


class Utils:

	@staticmethod
	def setupLogger():
		logger = logging.getLogger('linkedin')
		logger.propagate = False
		handler = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		logger.setLevel(logging.DEBUG)
		Utils.logger = logger
		return logger

	@staticmethod
	def getLogger():
		try:
			return Utils.logger
		except AttributeError:
			return Utils.setupLogger()

	@staticmethod
	def persistentPublicProfiles(profiles):
		pass
		# public_profile_file = open('./result/public_profile.pickle', 'ab')
		# if type(profiles) is list:
		# 	Utils.getLogger().debug('dump to public_profile.pickle %s - %s', profiles[0].file_name, profiles[-1].file_name)
		# else:
		# 	Utils.getLogger().debug('dump to public_profile.pickle %s', profiles.file_name)
		# pickle.dump(profiles, public_profile_file)
		# public_profile_file.close()

	@staticmethod
	def persistentCompanyProfiles(profiles):
		pass
		# company_profile_file = open('./result/company_profile.pickle', 'ab')
		#
		# if type(profiles) is list:
		# 	Utils.getLogger().debug('dump to company_profile.pickle %s - %s', profiles[0].file_name, profiles[-1].file_name)
		# else:
		# 	Utils.getLogger().debug('dump to company_profile.pickle %s', profiles.file_name)
		#
		# pickle.dump(profiles, company_profile_file)
		# company_profile_file.close()

	@staticmethod
	def persistentSkills(dir="./resources/skill/"):
		skills = []
		for f in os.listdir(dir):
			fpath = os.path.join(dir, f)
			sp = html_parser.SkillParser(fpath)
			skills.extend(sp.getSkills())
		skfile = open('./resources/skill/skill.pickle', 'wb')
		pickle.dump(skills, skfile)
	
	@staticmethod
	def levenshteinDistance(string1, string2):
		len1, len2 = len(string1), len(string2)
		if len1 > len2:
			string1, string2 = string2, string1
			len1, len2 = len2, len1

		current = range(len1 + 1)
		for i in range(1, len2 + 1):
			previous, current = current, [i] + [0] * len1
			for j in range(1, len1 + 1):
				add, delete = previous[j] + 1, current[j - 1]+1
				change = previous[j-1]
				if string1[j - 1] != string2[i - 1]:
					change += 1
				current[j] = min(add, delete, change)
		return current[len1]

	#not finish yet
	@staticmethod
	def getLatLngCityByName(company_name):
		_request_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&components=country:IE'
		address = urllib2.quote(company_name)
		url = _request_url % address

		data = json.load(urllib2.urlopen(url))

	@staticmethod
	def putExtraProfilesIntoDB(links, postfix='.htm'):
		for link in links:
			name = link.rsplit('/', 1)[1]
			try:
				# meaning this file is not downloaded yet, need to update it when we download
				DBHelper().dataAddEntry(name + postfix, link, False)
			except sqlite3.IntegrityError as e:
				print e.message
				print 'database error'
				traceback.print_exc()

if __name__ == '__main__':
	print Utils.levenshteinDistance('abc', 'abd')
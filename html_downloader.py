import urllib
from google import search
import string
from html_parser import PublicProfileParser, SkillParser, IrishNameParser
from profile_cleaner import ProfileCleaner
from db_helper import DBHelper
import sqlite3
import sys
import os
import traceback
from utils import Utils
import time

NUM = 10


class HTMLDownloader:
	# Download the html and store to a location specified by file_name
	@staticmethod
	def download(url, file_name):
		if os.path.exists(file_name):
			return

		wp = urllib.urlopen(url)

		wp_stream = wp.read()

		wp_file = open(file_name, 'w')
		wp_file.write(wp_stream)

		wp.close()
		wp_file.close()


class CompanyProfileDownloader:
	_default_folder = 'company_raw/'
	_default_postfix = '.htm'

	@staticmethod
	def downloadByUrl(url, file_name):
		full_path = CompanyProfileDownloader._default_folder + file_name + CompanyProfileDownloader._default_postfix
		if not os.path.exists(full_path):
			HTMLDownloader.download(url, full_path)
		return full_path

	def downloadByDiscovery(self):
		pass


class PublicProfileDownloader:
	_linkedin_ireland_url = 'http://ie.linkedin.com/in/'

	# Just like in Google, type: "keyword site:http://ie.linkedin.com/in/"
	# and download the content from return ulrs
	def googleSearch(self, keywords, site=_linkedin_ireland_url, num=NUM):
		urls = []
		urls[:] = search(keywords + ' ' + 'site:' + site, stop=num)

		urls[:] = (str(value) for value in urls if str(value).startswith(self._linkedin_ireland_url) == True)
		return urls

	# Search and Download
	def download(self, keyword):
		urls = self.googleSearch(keyword)

		for url in urls:
			self.downloadAndAnalyze(url)

	def downloadAndAnalyze(self, url, path='./user_raw/', postfix='.htm', analysis=True):
		file_name = Utils.getFileNameFromUrl(url)
		# if not DBHelper.dataInDB(file_name + postfix):
		if not os.path.exists(path + file_name + postfix):
			try:
				HTMLDownloader.download(url, path + file_name + postfix)
				if analysis:
					DBHelper().dataAddEntry(file_name + postfix, url, True)
					parser = PublicProfileParser(path + file_name + postfix)
					links = parser.getExtraProfiles()
					Utils.putExtraProfilesIntoDB(links)
				cleaner = ProfileCleaner(path+file_name+postfix)
				cleaner.saveToFile(path+file_name+postfix)

				# meaning this file is downloaded
			except sqlite3.IntegrityError:
				traceback.print_exc()
				pass
			except AttributeError:
				traceback.print_exc()
				os.remove(path + file_name + postfix)
		else:
			print 'file already exists'


# Download skills from research gate
class SkillDownloader:
	_research_gate_topic_url = 'https://www.researchgate.net/topics/'
	_folder_path = './resources/'

	def download(self, site=_research_gate_topic_url, store_path=_folder_path, postfix='.htm'):
		html_downloader = HTMLDownloader()
		for c in string.uppercase:
			url = site + c + '/'
			path = store_path + 'skill/' + c + postfix
			html_downloader.download(url, path)
			parser = SkillParser(path)
			pages = parser.getNumberOfPages()
			for i in range(2, pages + 1):
				url = site + c + '/?page=' + str(i)
				path = store_path + 'skill/' + c + '_' + str(i) + postfix
				html_downloader.download(url, path)


def main(argv):
	params = argv
	if len(params) == 1:
		params = IrishNameParser().names
	else:
		params = argv[1:]

	counter = 0
	profile_downloader = PublicProfileDownloader()
	for param in params:
		profile_downloader.download(param)
		counter += NUM
		if counter > 500:
			time.sleep(120)
			counter -= 500

	DBHelper.commitAndClose()

if __name__ == "__main__":
	main(sys.argv)

# if __name__ == "__main__":
# 	skd = SkillDownloader()
# 	skd.download()
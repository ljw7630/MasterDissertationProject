import sys
import os
#sys.path.insert(0, os.path.realpath('../../..'))
from html_parser import PublicProfileParser
import re


class ProfileCleaner:
	def __init__(self, file_name):
		self.parser = PublicProfileParser(file_name)
		self.file_name = file_name.split('/')[-1]
		given_name = self.parser.getGivenName()
		family_name = self.parser.getFamilyName()
		self.removeName(given_name, family_name)
		self.removeScripts()
		self.removeImage()
		self.removeExtra()
		self.removeGroups()
		self.removeHeader()
		self.removeFooter()

	def removeName(self, given_name, family_name):
		for item in self.parser.soup.find_all(text=re.compile(given_name+"\s*")):
			to_be_replace = item.replace('Jinwu', 'unknown')
			item.replace_with(to_be_replace)

		for item in self.parser.soup.find_all(text=re.compile("[a-zA-Z0-9]*"+family_name+"*")):
			to_be_replace = item.replace('Li', 'unknown')
			item.replace_with(to_be_replace)

	def removeScripts(self):
		for item in self.parser.soup.find_all('script'):
			item.extract()

	def removeSummary(self):
		tag = self.parser.soup.find('div', id='profile-summary')
		tag.extract()

	def removeImage(self):
		tag = self.parser.soup.find('img', class_="photo")
		tag.extract()

	def removeExtra(self):
		tag = self.parser.soup.find('div', id='extra')
		tag.extract()

	def removeGroups(self):
		tag = self.parser.soup.find('dt', class_='pubgroups')
		tag.extract()

		tag = self.parser.soup.find('dd', class_='pubgroups')
		tag.extract()

	def removeHeader(self):
		tag = self.parser.soup.find('div', id='header')
		tag.extract()

	def removeFooter(self):
		tag = self.parser.soup.find('div', id='footer')
		tag.extract()

	def saveToFile(self):

		f = open(os.path.realpath('survey/tmp/') + '/' + self.file_name, 'w')
		f.write(str(self.parser.soup))
		f.close()
		return os.path.basename(f.name)


def main():
	for fname in sys.argv[1:]:
		cleaner = ProfileCleaner(fname)
		cleaner.saveToFile()


if __name__ == '__main__':
	main()

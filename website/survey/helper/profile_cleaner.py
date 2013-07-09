import sys
sys.path.insert(0, '/home/ubuntu/MasterDissertationProject')
from html_parser import PublicProfileParser
import re
import os


class ProfileCleaner:
	def __init__(self, file_name):
		self.parser = PublicProfileParser(file_name)
		self.file_name = file_name.split('/')[-1]
		given_name = self.parser.getGivenName()
		family_name = self.parser.getFamilyName()
		self.removeName(given_name, family_name)
		self.removeImage()
		self.removeExtra()
		self.removeGroups()
		self.removeHeader()

	def removeName(self, given_name, family_name):
		for item in self.parser.soup.find_all(text=re.compile(given_name+"\s*")):
			to_be_replace = item.replace('Jinwu', 'unknown')
			item.replace_with(to_be_replace)

		for item in self.parser.soup.find_all(text=re.compile("[a-zA-Z0-9]*"+family_name+"*")):
			to_be_replace = item.replace('Li', 'unknown')
			item.replace_with(to_be_replace)

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

	def saveToFile(self):

		f = open('../tmp/' + self.file_name, 'w')
		f.write(str(self.parser.soup))
		f.close()
		return os.path.basename(f.name)


def main():
	for fname in sys.argv[1:]:
		cleaner = ProfileCleaner(fname)
		cleaner.saveToFile()


if __name__ == '__main__':
	main()

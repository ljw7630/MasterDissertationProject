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
		self.removeLinks()
		self.removeImage()
		#self.removeExtra()
		self.removeGroups()
		self.removeHeader()
		self.removeFooter()
		self.removeAdditional()
		self.removeContact()
		self.removeViewFullProfile()
		self.removeJoinLinkedIn()

	def removeName(self, given_name, family_name):
		for item in self.parser.soup.find_all(text=re.compile(given_name+"\s*")):
			to_be_replace = item.replace(given_name, 'unknown')
			item.replace_with(to_be_replace)

		for item in self.parser.soup.find_all(text=re.compile("[a-zA-Z0-9]*"+family_name+"*")):
			to_be_replace = item.replace(family_name, 'unknown')
			item.replace_with(to_be_replace)

	def removeScripts(self):
		for item in self.parser.soup.find_all('script'):
			item.extract()

	def removeLinks(self):
		for item in self.parser.soup.find_all("link"):
			item.extract()

	def removeSummary(self):
		tag = self.parser.soup.find('div', id='profile-summary')
		if tag:
			tag.extract()()

	def removeImage(self):
		tag = self.parser.soup.find('img', class_="photo")
		if tag:
			tag.extract()()

	def removeExtra(self):
		tag = self.parser.soup.find('div', id='extra')
		if tag:
			tag.extract()()

	def removeGroups(self):
		tag = self.parser.soup.find('dt', class_='pubgroups')
		if tag:
			tag.extract()()

		tag = self.parser.soup.find('dd', class_='pubgroups')
		if tag:
			tag.extract()()

	def removeHeader(self):
		tag = self.parser.soup.find('div', id='header')
		if tag:
			tag.extract()()

	def removeFooter(self):
		tag = self.parser.soup.find('div', id='footer')
		if tag:
			tag.extract()

	def removeViewFullProfile(self):
		tag = self.parser.soup.find('div', class_='view-full-profile')
		if tag:
			tag.extract()

	def removeRegForm(self):
		tag = self.parser.soup.find('div', id='blueregform')
		if tag:
			tag.extract()

	def removeAdditional(self):
		tag = self.parser.soup.find('div', id='profile-additional')
		if tag:
			tag.extract()

	def removeContact(self):
		tag = self.parser.soup.find('div', id='profile-contact')
		if tag:
			tag.extract()

	def removeJoinLinkedIn(self):
		tag = self.parser.soup.find('div', class_='join-linkedin')
		if tag:
			tag.extract()

	def saveToFile(self, file_name):
		f = open(file_name, 'w')
		f.write(str(self.parser.soup))
		f.close()
		return os.path.basename(f.name)


def main():
	for fname in sys.argv[1:]:
		cleaner = ProfileCleaner(fname)
		cleaner.saveToFile()


if __name__ == '__main__':
	main()

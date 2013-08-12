import sys
import os
import re
import bs4


class SurveyProfileCleaner:
	def __init__(self, file_name):
		self.soup = bs4.BeautifulSoup(open(file_name), from_encoding='utf-8')
		self.file_name = file_name.split('/')[-1]
		self.full_path = file_name
		self.removeOverview()
		self.removeSummary()
		self.removePublications()
		self.removeCourses()
		self.removeProjects()
		self.removeSkills()
		self.removeHonors()
		self.removeScripts()
		self.removeLinks()
		self.removeImage()
		self.removeExtra()
		self.removeGroups()
		self.removeHeader()
		self.removeFooter()
		self.removeAdditional()
		self.removeContact()
		self.removeViewFullProfile()
		self.removeJoinLinkedIn()

	def removeProjects(self):
		projects = self.soup.find('div', id='profile-projects')
		if projects:
			projects.extract()

	def removeSkills(self):
		skills = self.soup.find('div', id='profile-skills')
		if skills:
			skills.extract()

	def removeCourses(self):
		courses = self.soup.find('div', id='profile-courses')
		if courses:
			courses.extract()

	def removeOverview(self):
		overview = self.soup.find('h2', class_='section-title')
		if overview:
			overview.extract()

		dl = self.soup.find('dl', id='overview')
		if dl:
			dl.extract()

	def removeSummary(self):
		summary = self.soup.find('div', id='profile-summary')
		if summary:
			summary.extract()

	def removePublications(self):
		publications = self.soup.find('div', id='profile-publications')
		if publications:
			publications.extract()

	def removeHonors(self):
		honors = self.soup.find('div', id='profile-honorsawards')
		if honors:
			honors.extract()

	def removeScripts(self):
		for item in self.soup.find_all('script'):
			item.extract()

	def removeLinks(self):
		for item in self.soup.find_all("link"):
			item.extract()

	def removeSummary(self):
		tag = self.soup.find('div', id='profile-summary')
		if tag:
			tag.extract()()

	def removeImage(self):
		tag = self.soup.find('img', class_="photo")
		if tag:
			tag.extract()()

	def removeExtra(self):
		tag = self.soup.find('div', id='extra')
		if tag:
			tag.extract()()

	def removeGroups(self):
		tag = self.soup.find('dt', class_='pubgroups')
		if tag:
			tag.extract()()

		tag = self.soup.find('dd', class_='pubgroups')
		if tag:
			tag.extract()()

	def removeHeader(self):
		tag = self.soup.find('div', id='header')
		if tag:
			tag.extract()()

	def removeFooter(self):
		tag = self.soup.find('div', id='footer')
		if tag:
			tag.extract()

	def removeViewFullProfile(self):
		tag = self.soup.find('div', class_='view-full-profile')
		if tag:
			tag.extract()

	def removeRegForm(self):
		tag = self.soup.find('div', id='blueregform')
		if tag:
			tag.extract()

	def removeAdditional(self):
		tag = self.soup.find('div', id='profile-additional')
		if tag:
			tag.extract()

	def removeContact(self):
		tag = self.soup.find('div', id='profile-contact')
		if tag:
			tag.extract()

	def removeJoinLinkedIn(self):
		tag = self.soup.find('div', class_='join-linkedin')
		if tag:
			tag.extract()

	def saveToFile(self, file_name=None):
		if not file_name:
			file_name = self.full_path
		f = open(file_name, 'w')
		f.write(str(self.soup))
		f.close()
		return os.path.basename(f.name)

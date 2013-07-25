from __future__ import print_function
import bs4
from collections import defaultdict
from utils import Utils
from model import PersonalProfile, CompanyProfile


class IrishNameParser:
	_file_names = ['./resources/Irish_Boys_Names.htm', './resources/Irish_Girls_Names.htm']

	def __init__(self):
		self.names = []

		for file_name in self._file_names:
			self.getNames(file_name)

	def getNames(self, file_name):
		soup = bs4.BeautifulSoup(open(file_name))
		tr_names = soup.find('tbody').findAll('tr')[3:]

		for tr_name in tr_names:
			name = tr_name.findAll('td')[1].font.string
			self.names.append(name)


class DegreeAbbreviationParser:
	_file_name = './resources/British degree abbreviations - Wikipedia, the free encyclopedia.html'

	def __init__(self):
		self.soup = bs4.BeautifulSoup(open(self._file_name))
		self.getAllAbbrs()

	def getBachelorDegreeAbbrs(self):

		degree_list = self.soup.find("a", text="Bachelor's degree").findNext('ul').findAll('li')

		return self.getDegreeMapFromList(degree_list)

	def getMasterDegreeAbbrs(self):
		degree_list = self.soup.find('span', text='Postgraduate degrees', id='Postgraduate_degrees').findNext(
			'ul').findAll('li')

		postgraduate_degrees = self.getDegreeMapFromList(degree_list)

		# remove duplicate 'MA'
		degree_list = self.soup.find('span', text="Master's degrees", id='Master.27s_degrees').findNext('ul').findAll(
			'li')[1:]

		master_degrees = self.getDegreeMapFromList(degree_list)

		return dict(postgraduate_degrees.items() + master_degrees.items())

	def getDoctorDegreeAbbrs(self):
		degree_list = self.soup.find('span', text='Junior (Professional) Doctorates',
		                             id='Junior_.28Professional.29_Doctorates').findNext('ul').findAll('li')

		degree_list.extend(
			self.soup.find('span', text='Intermediate Doctorates', id='Intermediate_Doctorates').findNext('ul').findAll(
				'li'))

		degree_list.extend(
			self.soup.find('span', text='Higher Doctorates', id='Higher_Doctorates').findNext('ul').findAll('li'))

		return self.getDegreeMapFromList(degree_list)

	def getDegreeMapFromList(self, degree_list):

		degree_map = {}

		for degree in degree_list:
			# remove hyperlink
			while degree.a is not None:
				degree.a.replace_with(degree.a.string)

			abbreviation, name = degree.text.split('-')
			abbreviations = abbreviation.replace(',', ' ').replace(' or ', ' ').replace('/', ' ').split()
			abbreviations = [abbr.strip() for abbr in abbreviations]
			name = name.strip().replace(' ', '_')

			degree_map[name] = abbreviations
		return degree_map

	def saveToFile(self):
		f = open('resources/degree_abbrs.txt', 'w')

		# bd = self.getBachelorDegreeAbbrs()
		# self.unfoldToLine(f, 8, bd)
		#
		# md = self.getMasterDegreeAbbrs()
		# self.unfoldToLine(f, 9, md)
		#
		# phd = self.getDoctorDegreeAbbrs()
		# self.unfoldToLine(f, 10, phd)
		#
		# f.close()

		for linearr in self.degrees:
			line = " ".join(linearr)
			f.write(line + '\n')
		f.close()

	# convert a map to a line of words
	# def unfoldToLine(self, f, level, dictionary):
	# 	for key in dictionary.keys():
	# 		arr = dictionary[key]
	# 		line = str(level) + " " + " ".join(arr) + " " + key
	# 		f.write(line + '\n')

	def getAllAbbrs(self):
		bg = self.getBachelorDegreeAbbrs()
		mg = self.getMasterDegreeAbbrs()
		dg = self.getDoctorDegreeAbbrs()

		self.degrees = []
		self.unfold(bg, 8, self.degrees)
		self.unfold(mg, 9, self.degrees)
		self.unfold(dg, 10, self.degrees)
		self.dictionary = dict(bg.items() + mg.items() + dg.items())

	def unfold(self, dictionary, level, degrees):
		for key in dictionary.keys():
			arr = dictionary[key]
			degrees.append([str(level)] + arr + [key])


class IndustryParser:
	_file_name = './resources/industry.html'

	def getIndustries(self):
		self.soup = bs4.BeautifulSoup(open(self._file_name))
		options = self.soup.findAll('option')
		option_list = []
		for option in options[1:]:
			option_list.append(option.string.replace('/', ' and '))
		return option_list


class DisciplineParser:
	_file_name = './resources/List of academic disciplines - Wikipedia.html'

	def getDisciplinesHierarchy(self):
		soup = bs4.BeautifulSoup(open(self._file_name))

		h2s = soup.findAll('h2')

		h2s = h2s[2:-5]
		disciplines = defaultdict(dict)
		for h2 in h2s:
			disciplines[h2.span.string] = {}
			h3 = h2.findNext('h3')
			while h3.findPrevious('h2') == h2:
				disciplines[h2.span.string][h3.span['id']] = {}
				table = h3.findNext('table')
				tds = table.findAll('td')
				for td in tds:
					ul = td.find('ul')
					tmp_dicts = self.getUlDict(ul)
					disciplines[h2.span.string][h3.span['id']].update(tmp_dicts)
				h3 = h3.findNext('h3')
		return disciplines

	def getUlDict(self, ul):
		dicts = defaultdict(dict)
		li = ul.find('li')
		while True:
			try:
				if li.next_element.name == 'a':
					dicts[li.a.string] = {}
			except AttributeError:
					dicts[li.next_element] = {}
			# if li.a:
			# 	dicts[li.a.string] = {}
			# else:
			# 	dicts[li.string] = {}
			if li.find('ul') is not None:
				dicts[li.a.string] = self.getUlDict(li.ul)
			if li.findNextSibling('li') is None:
				break
			li = li.findNextSibling('li')
		return dicts


class SkillParser:
	def __init__(self, file_name):
		self.soup = bs4.BeautifulSoup(open(file_name))

	def getNumberOfPages(self):
		pages = self.soup.findAll("a", class_="navi-page-link pager-link")
		if not pages:
			return 1
		else:
			return int(pages[-1].string.strip())

	def getSkills(self):
		skills = []
		lis = self.soup.findAll("li", class_="publictopics-TopicItem")
		for li in lis:
			skills.append(li.div.a.string.strip())
		return skills


class CompanyProfileParser:

	def __init__(self, file_name):
		Utils.getLogger().debug(file_name)
		self.soup = bs4.BeautifulSoup(open(file_name))
		self.file_name = file_name

	def parseHtml(self):
		basic_infos = self.soup.find('div', class_="basic-info").dl.findAll('dt')

		self.content = {}
		for info in basic_infos:
			dd = info.findNext('dd')
			value = dd.string.strip() if dd.a is None else dd.a.string.strip()
			self.content[info.string.strip()] = value

		company_profile = CompanyProfile()
		company_profile.content = self.content
		company_profile.file_name = self.file_name

		return company_profile


class PublicProfileParser:
	_linkedin_url_prefix = 'http://www.linkedin.com'
	_linkedin_ireland_url_prefix = 'http://ie.linkedin.com'

	def __init__(self, file_name):
		Utils.getLogger().debug(file_name)
		self.soup = bs4.BeautifulSoup(open(file_name))
		self.file_name = file_name.split('/')[-1]

	def parseHtml(self):
		profile = PersonalProfile()
		profile.file_name = self.file_name
		# profile.given_name = self.getGivenName()
		# profile.family_name = self.getFamilyName()
		profile.industry = self.getIndustry()
		profile.headline_title = self.getHeadlineTitle()
		profile.experience_list = self.getExperiences()

		profile.website_list = self.getWebsites()
		profile.language_list = self.getLanguages()
		profile.skill_list = self.getSkills()
		profile.education_list = self.getEducations()
		profile.extra_profile_list = self.getExtraProfiles()

		return profile

	def getGivenName(self):
		given_name_with_tag = self.soup.find("span", class_="given-name")
		given_name = given_name_with_tag.string
		return given_name

	def getFamilyName(self):
		family_name_with_tag = self.soup.find("span", class_="family-name")
		family_name = family_name_with_tag.string
		return family_name

	def getIndustry(self):
		industry = self.soup.find('dd', class_='industry')

		if industry is not None:
			industry = industry.string.strip()
		return industry

	def getHeadlineTitle(self):
		headline_title_with_tag = self.soup.find("p", class_="headline-title title")
		headline_title = None
		if headline_title_with_tag is not None:
			headline_title = headline_title_with_tag.string.strip()
		return headline_title

	def getExperiences(self):
		profile_experience = self.soup.find("div", id="profile-experience")
		experience_list = []
		if profile_experience is not None:

			raw_experiences = profile_experience.find('div', 'content vcalendar').findAll('div', 'position')
			for raw_experience in raw_experiences:
				job_title = raw_experience.div.h3.span.string.strip()
				company = raw_experience.div.h4.strong
				experience = {'job_title': job_title}
				if company.a is not None:
					company_url = self._linkedin_url_prefix + company.a['href']
					company_name = company.a.span.string.strip()
					experience['company_url'] = company_url
					experience['company_name'] = company_name
				else:
					company_name = company.span.string.strip()
					experience['company_name'] = company_name

				period_raw = raw_experience.find('p', 'period')
				self.getFromTo(experience, period_raw)

				experience_list.append(experience)
		return experience_list

	def getWebsites(self):
		ul = self.soup.find("dd", class_="websites")

		websites = []

		if ul is not None:
			website_list = ul.findAll('li')

			for website in website_list:
				href = website.a['href']
				name = website.a.string.strip()
				if href.startswith('/redir'):
					href = self._linkedin_url_prefix + href
				websites.append({'website_name': name, 'url': href})

		return websites

	def getLanguages(self):
		lis = self.soup.find("ul", class_="languages competencies")

		language_list = []

		if lis is not None:

			languages = lis.findAll('li')

			for language_tag in languages:
				language = language_tag.h3.string
				language_list.append(language.encode('utf-8'))

		return language_list

	def getSkills(self):
		skills = self.soup.find("ol", class_="skills")

		skill_list = []

		if skills is not None:
			lis = skills.findAll('li')

			for li in lis:
				href = li.span.a['href']
				skill = li.span.a.string.strip()
				skill_list.append({'skill': skill, 'url': href})

		return skill_list

	def getEducations(self):
		details = self.soup.find("div", class_="section subsection-reorder summary-education")
		detail_list = []

		if details is not None:
			mainDiv = details.find('div', class_='content vcalendar')

			divs = mainDiv.findAll('div')

			for div in divs:
				collegeTitle = div.h3.string.strip()
				detailsEducation = div.h4.findAll('span')
				education_dictionary = {'college': collegeTitle}
				for item in detailsEducation:
					key = item['class'][0]
					value = item.string.strip()
					education_dictionary[key] = value

				period_raw = div.find('p', 'period')
				if period_raw:
					self.getFromTo(education_dictionary, period_raw)

				detail_list.append(education_dictionary)

		return detail_list

	def getExtraProfiles(self):
		profiles = self.soup.findAll('li', class_='with-photo')

		extra_profile_list = []
		for profile in profiles:
			url = profile.strong.a['href']
			url = url[:url.find('?')]
			url = '/'.join(url.split('/')[:5])
			if str(url).startswith(self._linkedin_ireland_url_prefix):

				extra_profile_list.append(url)
				# name = profile.strong.a.string.strip()
				#
				# if profile.span.string is not None:
				# 	headline_title = profile.span.string.strip()
				# 	extra_profile_list.append({'url': url, 'name': name, 'headline_title': headline_title})
				# else:
				# 	extra_profile_list.append({'url': url, 'name': name})

		return extra_profile_list

	def getFromTo(self, dictionary, period_raw):
		from_to = period_raw.findAll('abbr')

		if from_to:
			try:
				dictionary['from'] = from_to[0]['title']
				dictionary['to'] = from_to[1]['title']
			except IndexError:
				pass
		else:
			dictionary['from'] = period_raw.string.strip()

	def removeNewlineInList(self, alist):
		return (value for value in alist if value != u'\n')

	def getStringContentsInList(self, alist):
		return (value.string.strip() for value in alist)

	def __str__(self):
		return "Name: " + self.given_name + " " + self.family_name + "\n" \
			+ "Industry: " + self.industry + "\n" \
			+ "Experiences: " + str(self.experience_list) + "\n" \
			+ "Educations: " + str(self.education_detail_list) + "\n" \
			+ "Languages: " + str(self.language_list) + "\n" \
			+ "Skills: " + str(self.skill_list) + "\n"


def main():
	dp = DisciplineParser()
	print(dp.getDisciplinesHierarchy())


if __name__ == "__main__":
	main()
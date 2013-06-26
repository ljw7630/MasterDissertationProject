from __future__ import print_function
import bs4
from collections import defaultdict


class DegreeAbbreviationParser:
	_file_name = './resources/British degree abbreviations - Wikipedia, the free encyclopedia.html'

	def __init__(self):
		self.soup = bs4.BeautifulSoup(open(self._file_name))

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
			name = name.strip()

			degree_map[name] = abbreviations
		return degree_map


class IndustryParser:
	_file_name = './resources/industry.html'

	def getIndustries(self):
		soup = bs4.BeautifulSoup(open(self._file_name))
		options = soup.findAll('option')
		option_list = []
		for option in options[1:]:
			option_list.append(option.string)
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
				disciplines[h2.span.string][h3.span.string] = {}
				table = h3.findNext('table')
				tds = table.findAll('td')
				for td in tds:
					ul = td.find('ul')
					tmp_dicts = self.getUlDict(ul)
					disciplines[h2.span.string][h3.span.string].update(tmp_dicts)
				h3 = h3.findNext('h3')
		return disciplines

	def getUlDict(self, ul):
		dicts = defaultdict(dict)
		li = ul.find('li')
		while True:
			if li.a:
				dicts[li.a.string] = {}
			else:
				dicts[li.string] = {}
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


# main handler, open the file, and parse each section

# comment: at the moment, current experience and past experience return not the same structures and contents

class PublicProfileParser:
	_linkedin_url_prefix = 'http://www.linkedin.com'
	_linkedin_ireland_url_prefix = 'http://ie.linkedin.com'

	def __init__(self, file_name):
		self.soup = bs4.BeautifulSoup(open(file_name))

	def parseHtml(self):
		self.given_name = self.getGivenName()
		self.family_name = self.getFamilyName()
		self.industry = self.getIndustry()
		self.headline_title = self.getHeadlineTitle()
		self.current_experience = self.getCurrentExperience()
		self.past_experience_list = self.getPastExperience()

		self.education_list = self.getEducation()
		self.website_list = self.getWebsites()
		self.language_list = self.getLanguages()
		self.skill_list = self.getSkills()
		self.education_detail_list = self.getEducationDetails()
		self.extra_profile_list = self.getExtraProfiles()

		# print(
		# 	given_name, family_name, industry, headline_title, \
		# 	current_experience, past_experience_list, \
		# 	education_list, website_list, \
		# 	language_list, skill_list, education_detail_list, \
		# 	extra_profile_list, sep='\n')

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
		headline_title = headline_title_with_tag.string.strip()
		return headline_title

	def getCurrentExperience(self):
		current = self.soup.find("div", class_="summary-current")
		if current is None:
			return None
		postitle = current.find("div", class_="postitle")
		job_title = postitle.h3.span.string.strip()
		company = postitle.h4.strong

		current_experience = {'job_title': job_title}

		# this company has no hyperlink

		if company.a is not None:
			company_url = self._linkedin_url_prefix + company.a['href']
			company_name = company.a.span.string.strip()
			current_experience['company_url'] = company_url
			current_experience['company_name'] = company_name
		else:
			company_name = company.string.strip()
			current_experience['company_name'] = company_name

		period_raw = current.find("p", class_="period")
		from_to = period_raw.findAll("abbr")

		if not from_to:
			period = period_raw.string.strip()
			current_experience['from'] = period
		else:
			start = from_to[0].string.strip()
			end = from_to[1].string.strip()
			current_experience['from'] = start
			current_experience['to'] = end

		return current_experience

	def getPastExperience(self):
		lis = self.soup.find("ul", class_="past")

		past_experience_list = []

		if lis is not None:
			lis = lis.findAll('li')

			for li in lis:
				nonempty_list = []
				nonempty_list[:] = self.removeNewlineInList(li.contents)
				title = nonempty_list[0].string.strip()
				company_name = nonempty_list[2].string.strip()
				if type(nonempty_list[2]) == bs4.element.Tag:
					company_url = self._linkedin_url_prefix + nonempty_list[2]['href']
				else:
					company_url = None

				past_experience_list.append(
					{'job_title': title, 'company_name': company_name, 'company_url': company_url})

		return past_experience_list

	def getEducation(self):
		ul = self.soup.find("dd", class_="summary-education")
		education_list = []

		if ul is not None:
			lis = ul.findAll('li')
			for li in lis:
				if len(li.contents) == 1:
					education_list.append(li.string.strip())
				# if the education lists more than three schools, there're some hidden elements
				elif len(li.contents) == 3:
					education_list.append(li.div.string.strip())

		return education_list

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
			languages = []
			languages[:] = self.removeNewlineInList(lis)

			for language_tag in languages:
				language = language_tag.h3.string
				language_list.append(language)

		return language_list

	def getSkills(self):
		skills = self.soup.find("ol", class_="skills")

		skill_list = []

		if skills is not None:
			lis = []
			lis[:] = self.removeNewlineInList(skills)
			for li in lis:
				href = li.span.a['href']
				skill = li.span.a.string.strip()
				skill_list.append({'skill': skill, 'url': href})

		return skill_list

	def getEducationDetails(self):
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
				detail_list.append(education_dictionary)

		return detail_list

	def getExtraProfiles(self):
		profiles = self.soup.findAll('li', class_='with-photo')

		extra_profile_list = []
		for profile in profiles:
			url = profile.strong.a['href']

			if str(url).startswith(self._linkedin_ireland_url_prefix):
				name = profile.strong.a.string.strip()
				headline_title = profile.span.string.strip()
				extra_profile_list.append({'url': url, 'name': name, 'headline_title': headline_title})

		return extra_profile_list

	def removeNewlineInList(self, alist):
		return (value for value in alist if value != u'\n')

	def getStringContentsInList(self, alist):
		return (value.string.strip() for value in alist)


def main():
	dp = DisciplineParser()
	print(dp.getDisciplinesHierarchy())


if __name__ == "__main__":
	main()
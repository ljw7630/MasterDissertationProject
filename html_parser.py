from __future__ import print_function
import bs4
import sys


linkedIn_url_prefix = 'http://www.linkedin.com'
linkedin_ireland_url_prefix = 'http://ie.linkedin.com'

# main handler, open the file, and parse each section

# comment: at the moment, current experience and past experience return not the same structures and contents

class html_parser:
	def __init__(self, file_name)
		self.soup = bs4.BeautifulSoup(open(file_name))
		
	def parseHtml(file_name):		
		given_name = getGivenName()
		family_name = getFamilyName()
		industry = getIndustry()
		headline_title = getHeadlineTitle()
		current_experience = getCurrentExperience()
		past_experience_list = getPastExperience()

		education_list = getEducation()
		website_list = getWebsites()
		language_list = getLanguages()
		skill_list = getSkillsAndExpertise()
		education_detail_list = getEducationDetails()
		extra_profile_list = getExtraProfile()
		
		print (given_name, family_name, industry, headline_title, \
			cpast_experience_list, past_experience_list, \
			education_list, website_list, \
			language_list, skill_list, education_detail_list, \
			extra_profile_list, sep = '\n')


	def getGivenName():
		given_name_with_tag = self.soup.find("span", class_="given-name")
		given_name = given_name_with_tag.string
		return given_name

	def getFamilyName():
		family_name_with_tag = self.soup.find("span", class_="family-name")
		family_name = family_name_with_tag.string
		return family_name

	def getIndustry():
		industry = self.soup.find('dd', class_='industry')

		if industry != None:
			industry = industry.string.strip()
		return industry

	def getHeadlineTitle():
		headline_title_with_tag = self.soup.find("p", class_="headline-title title")
		headline_title = headline_title_with_tag.string.strip()
		return headline_title

	def getCurrentExperience():	
		current = self.soup.find("div", class_ = "summary-current")
		postitle = current.find("div", class_ = "postitle")
		job_title = postitle.h3.span.string.strip()
		company = postitle.h4.strong
		
		current_experience = {}
		
		current_experience['job_title'] = job_title
		
		# this company has no hyperlink

		if company.a != None:
			company_url = linkedIn_url_prefix + company.a['href']
			company_name = company.a.span.string.strip()
			current_experience['company_url'] = company_url
			current_experience['company_name'] = company_name
		else:
			company_name = company.string.strip()
			current_experience['company_name'] = company_name
			
		period_raw = current.find("p",class_="period")
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

	def getPastExperience():
		lis = self.soup.find("ul", class_ = "past")

		past_experience_list = []

		if lis != None:
			lis = lis.findAll('li')

			for li in lis:
				nonempty_list = []
				nonempty_list[:] = removeNewlineInList(li.contents)
				title = nonempty_list[0].string.strip()
				company_name = nonempty_list[2].string.strip()
				if type(nonempty_list[2]) == bs4.element.Tag:
					company_url = linkedIn_url_prefix + nonempty_list[2]['href']
				else:
					company_url = None

				past_experience_list.append({'job_title': title, 'company_name': company_name, 'company_url': company_url } )

		return past_experience_list

	def getEducation():
		ul = self.soup.find("dd", class_ = "summary-education")
		education_list = []

		if ul != None:	
			lis = ul.findAll('li')
			for li in lis:
				if len(li.contents) == 1:
					education_list.append(li.string.strip())
				# if the education lists more than three schools, there're some hidden elements
				elif len(li.contents) == 3:
					education_list.append(li.div.string.strip())

		return education_list

	def getWebsites():
		ul = self.soup.find("dd", class_ = "websites")

		websites = []

		if ul != None:
			website_list = ul.findAll('li')

			for website in website_list:
				href = website.a['href']
				name = website.a.string.strip()
				if href.startswith('/redir'):
					href = linkedIn_url_prefix + href
				websites.append({'website_name':name, 'url':href})
			
		return websites


	def getLanguages():
		lis = self.soup.find("ul", class_="languages competencies")

		language_list = []
		
		if lis != None:
			languages = []
			languages[:] = removeNewlineInList(lis)

			for language_tag in languages:
				language = language_tag.h3.string
				language_list.append(language)

		return language_list

	def getSkillsAndExpertise():
		skills = self.soup.find("ol", class_="skills")

		skill_list = []

		if skills != None:
			lis = []
			lis[:] = removeNewlineInList(skills)
			for li in lis:
				href = li.span.a['href']
				skill = li.span.a.string.strip()
				skill_list.append({'skill': skill, 'url': href})

		return skill_list
		
	def getEducationDetails():
		details = self.soup.find("div", class_ = "section subsection-reorder summary-education")
		detail_list = []

		if details != None:
			mainDiv = details.find('div', class_ = 'content vcalendar')

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

	def getExtraProfile():
		profiles = self.soup.findAll('li', class_ = 'with-photo')

		extra_profile_list = []
		for profile in profiles:
			url = profile.strong.a['href']		

			if str(url).startswith(linkedin_ireland_url_prefix) == True:			
				name = profile.strong.a.string.strip()
				headline_title = profile.span.string.strip()
				extra_profile_list.append({'url': url, 'name': name, 'headline_title':headline_title})

		return extra_profile_list	

	def removeNewlineInList(alist):
		return (value for value in alist if value != u'\n')

	def getStringContentsInList(alist):
		return (value.string.strip() for value in alist)

def main(argv):	
	for i in range(1, len(argv)):
		parseHtml(argv[i])

if __name__ == "__main__":
    main(sys.argv)
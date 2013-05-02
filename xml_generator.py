from bs4 import BeautifulSoup
dest_soup = bs4.BeautifulSoup()

class xml_generator:

	def __init__(self, parser, dest_soup):

		self.parser = parser
		self.dest_soup = dest_soup
		
		self.name_tag = dest_soup.new_tag("name")
		self.industry_tag = dest_soup.new_tag("industry")
		self.headline_tag = dest_soup.new_tag("headline")

		self.experience_tag = dest_soup.new_tag("experiences")
		#self.experience_sub_tag = dest_soup.new_tag("experience")
		#self.experience_job_title_tag = dest_soup.new_tag("experience_job_title")
		#self.experience_company_url_tag = dest_soup.new_tag("experience_company_url")
		#self.experience_company_name_tag = dest_soup.new_tag("experience_company_name")
		#self.experience_period_from_tag = dest_soup.new_tag("experience_period_from")
		#self.experience_period_to_tag = dest_soup.new_tag("experience_period_to")

		self.education_tag = dest_soup.new_tag("educations")
		#self.education_sub_tag = dest_soup.new_tag("education")
		#self.education_major_tag = dest_soup.new_tag("education_major")
		#self.education_college_tag = dest_soup.new_tag("education_college")
		#self.education_degree_tag = dest_soup.new_tag("education_degree")

		self.websites_tag = dest_soup.new_tag("websites")
		#self.websites_sub_tag = dest_soup.new_tag("website")
		#self.website_name_tag = dest_soup.new_tag("webiste_name")
		#self.webiste_url_tag = dest_soup.new_tag("url")

		self.language_tag = dest_soup.new_tag("language")
		self.skills_tag = dest_soup.new_tag("skills")
		#self.skills_sub_tag = dest_soup.new_tag("skill")
		#self.skill_name_tag = dest_soup.new_tag("skill_name")
		#self.skill_url_tag = dest_soup.new_tag("skill_url")

		self.extra_profile_tag = dest_soup.new_tag("extra_profiles")

	def insertName():
		self.name_tag.insert(0, self.parser.getGivenName() + " " + self.parser.getFamilyName()

	def insertIndustry():
		self.industry_tag.insert(0, self.parser.getIndustry())

	def inserHeadline():
		self.headline_tag.insert(0, self.parser.getHeadlineTitle())

	def insertExperience():
		experience_list = [self.parser.getCurrentExperience()] + self.parser.getPastExperience()
		for i in range(0, len(experience_list) ):
			experience_sub_tag = self.dest_soup.new_tag("experience")
			
			experience_job_title_tag = self.dest_soup.new_tag("experience_job_title")
			experience_company_url_tag = dest_soup.new_tag("experience_company_url")
			experience_company_name_tag = dest_soup.new_tag("experience_company_name")
			experience_period_from_tag = dest_soup.new_tag("experience_period_from")
			experience_period_to_tag = dest_soup.new_tag("experience_period_to")

			self.experience_tag.insert(i, experience_sub_tag)
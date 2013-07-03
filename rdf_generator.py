from schema_generator import SchemaGenerator as SG
from rdflib import BNode, RDF, Literal
from rdflib.namespace import FOAF, XSD
from html_parser import CompanyProfileParser as CPP
from html_downloader import CompanyProfileDownloader as CPD
from utils import Utils
import re


class RDFGenerator:
	colleges = set()
	languages = set()
	courses = set()
	degrees = set()
	skills = set()
	job_titles = set()
	companies = set()
	company_profiles = []

	def __init__(self):
		self.schema = SG()
		self.schema.generate()

	def graph_add(self, s, p, o):
		self.schema.graph.add((s, p, o))

	def add(self, profile):
		person = BNode()
		self.graph_add(person, RDF.type, FOAF.Person)

		self.add_language_triple(profile, person)
		self.add_skill_triple(profile, person)
		self.add_education_triple(profile, person)
		self.add_experience_triple(profile, person)

	def add_language_triple(self, profile, person):
		for language in profile.language_list:
			term = self.schema.get_term(language)

			# if this is the new language we encounter
			if language not in self.languages:
				self.graph_add(term, RDF.type, self.schema.Language)
				self.languages.add(language)

			self.graph_add(person, self.schema.language, term)

	def add_skill_triple(self, profile, person):
		for skill_dict in profile.skill_list:
			skill_name = skill_dict['skill']
			term = self.schema.get_term(skill_name)

			if skill_name not in self.skills:
				self.graph_add(term, RDF.type, self.schema.Skill)
				self.graph_add(term, RDF.type, self.schema.Concept)
				self.skills.add(skill_name)

			self.graph_add(person, self.schema.skill, term)

	def add_education_triple(self, profile, person):
		for education_dict in profile.education_list:
			education = BNode()

			if 'college' in education_dict:
				college = education_dict['college']
				term = self.schema.get_term(college)

				if college not in self.colleges:
					self.graph_add(term, RDF.type, self.schema.College)
					self.colleges.add(college)

				self.graph_add(education, self.schema.college, term)

			if 'major' in education_dict:
				course = education_dict['major']
				term = self.schema.get_term(course)

				if course not in self.courses:
					self.graph_add(term, RDF.type, self.schema.Course)
					self.graph_add(term, RDF.type, self.schema.Concept)
					self.colleges.add(course)

				self.graph_add(education, self.schema.major, term)

			if 'degree' in education_dict:
				degree = education_dict['degree']
				degree, level = self.degree_helper(degree)
				term = self.schema.get_term(degree)

				if degree not in self.degrees:
					self.graph_add(term, RDF.type, self.schema.Degree)
					self.graph_add(term, self.schema.level, Literal(level, datatype=XSD.interger))
					self.degrees.add(degree)

				self.graph_add(education, self.schema.degree, term)

			self.graph_add(person, self.schema.education, education)

	def add_experience_triple(self, profile, person):
		for experience in profile.experience_list:
			position = BNode()

			if 'job_title' in experience:
				job_title = experience['job_title']
				job_title = self.position_helper(job_title)
				term = BNode()

				self.graph_add(term, RDF.type, self.schema.Position)
				self.graph_add(term, self.schema.occupation, Literal(job_title))
				try:
					if experience['from'] and self.check_datetime_format(experience['from']):
						self.graph_add(term, self.schema.from_value, Literal(experience['from'], datatype=XSD.date))
				except KeyError:
					pass
				try:
					if experience['to'] and self.check_datetime_format(experience['to']):
						self.graph_add(term, self.schema.to_time, Literal(experience['to'], datatype=XSD.date))
				except KeyError:
					pass

			if 'company_name' in experience:
				company_name = experience['company_name']
				company_name = self.company_name_helper(company_name)
				company = self.schema.get_term(company_name)

				# we need to define this company
				if company_name not in self.companies:
					self.graph_add(company, RDF.type, self.schema.Organization)
					self.companies.add(company_name)

					# extra process required for
					if 'company_url' in experience:
						company_profile = self.get_company_profile(experience['company_url'], company_name).content

						if 'Founded' in company_profile:
							self.graph_add(company, self.schema.formation_year, Literal(company_profile['Founded'], datatype=XSD.gYear))

						if 'Company Size' in company_profile:
							mini, maxi = self.get_company_size(company_profile['Company Size'])
							self.graph_add(company, self.schema.from_value, Literal(mini, datatype=XSD.integer))
							self.graph_add(company, self.schema.to_time, Literal(maxi, datatype=XSD.integer))

						if 'Type' in company_profile:
							self.graph_add(company, self.schema.organization_type, Literal(company_profile['Type'], datatype=XSD.integer))

						if 'Industry' in company_profile:
							self.graph_add(company, self.schema.industry, self.schema.get_term(company_profile['Industry']))

						Utils.persistentCompanyProfiles(company_profile)

				self.graph_add(company, self.schema.has_position, position)
				self.graph_add(person, self.schema.works_as, position)

	def get_company_profile(self, url, company_name):
		file_path = CPD.downloadByUrl(url, company_name)
		parser = CPP(file_path)
		company_profile = parser.parseHtml()

		return company_profile

	def get_company_size(self, company_size_string):
		company_size_string = company_size_string.replace(',', '')
		match = re.search(r'([0-9]+)-([0-9]+)\s\w+', company_size_string)

		try:
			if match is None:
				match = re.search(r'([0-9]+)\+\s\w+', company_size_string)
				return int(match.group(1).replace(',', '')), 999999
			else:
				return int(match.group(1)), int(match.group(2))
		except AttributeError:
			return 1, 1


	def check_datetime_format(self, datetime_string):
		match = re.search(r'(\d{4}-\d{2}-\d{2})', datetime_string)
		return match

	def position_helper(self, position):
		return position

	def degree_helper(self, degree):
		return degree, 7

	def company_name_helper(self, company_name):
		return company_name

	def save(self, format='turtle', file_name='result/data.rdf'):
		f = open(file_name, 'wb')
		print >> f, self.schema.graph.serialize(format=format)
		f.close()
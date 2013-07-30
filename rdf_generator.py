from schema_generator import SchemaGenerator as SG
from rdflib import BNode, RDF, Literal, Graph, RDFS
from rdflib.namespace import FOAF, XSD
from html_parser import CompanyProfileParser as CPP, CityParser
from html_downloader import CompanyProfileDownloader as CPD
from utils import Utils
import re
import os
from socket_handler import DegreeSocketHandler, UniversitySocketHandler, LanguageSocketHandler
import pickle
from db_helper import DBHelper

RESOURCES_COLLEGES_PICKLE = 'resources/colleges.pickle'

RESOURCES_COMPANIES_PICKLE = 'resources/companies.pickle'

RESOURCES_COURSES_PICKLE = 'resources/courses.pickle'

RESOURCES_DEGREES_PICKLE = 'resources/degrees.pickle'

RESOURCES_JOB_TITLES_PICKLE = 'resources/job_titles.pickle'

RESOURCES_LANGUAGES_PICKLE = 'resources/languages.pickle'

RESOURCES_SKILLS_PICKLE = 'resources/skills.pickle'

RESOURCES_ONTOLOGY_OWL = 'result/ontology.owl'

RESOURCES_DATA_RDF = 'result/data.rdf'


class RDFGenerator:
	# company_profiles = []

	def __init__(self):
		self.schema = SG()
		if os.path.exists(RESOURCES_DATA_RDF):
			self.graph = Graph()
			self.graph.parse(RESOURCES_DATA_RDF, format='xml')

			print 'load % lines of triples' % len(self.graph)
		elif os.path.exists(RESOURCES_ONTOLOGY_OWL):
			self.graph = Graph()
			self.graph.parse(RESOURCES_ONTOLOGY_OWL, format='xml')
		else:
			self.schema.generate()
			self.graph = self.schema.graph
			print 'create a new graph'

		self.loadPickles()

		self.degree_socket_handler = DegreeSocketHandler()
		self.degree_socket_handler.send_query_command()
		self.university_socket_handler = UniversitySocketHandler()
		self.university_socket_handler.send_query_command()
		self.language_socket_handler = LanguageSocketHandler()
		self.language_socket_handler.send_query_command()

	def loadPickles(self):
		#loading pickles if exist
		if os.path.exists(RESOURCES_COLLEGES_PICKLE):
			self.colleges = pickle.load(open(RESOURCES_COLLEGES_PICKLE))
		else:
			self.colleges = set()

		if os.path.exists(RESOURCES_COMPANIES_PICKLE):
			self.companies = pickle.load(open(RESOURCES_COMPANIES_PICKLE))
		else:
			self.companies = set()

		if os.path.exists(RESOURCES_COURSES_PICKLE):
			self.courses = pickle.load(open(RESOURCES_COURSES_PICKLE))
		else:
			self.courses = set()

		if os.path.exists(RESOURCES_DEGREES_PICKLE):
			self.degrees = pickle.load(open(RESOURCES_DEGREES_PICKLE))
		else:
			self.degrees = set()

		if os.path.exists(RESOURCES_JOB_TITLES_PICKLE):
			self.job_titles = pickle.load(open(RESOURCES_JOB_TITLES_PICKLE))
		else:
			self.job_titles = set()

		if os.path.exists(RESOURCES_LANGUAGES_PICKLE):
			self.languages = pickle.load(open(RESOURCES_LANGUAGES_PICKLE))
		else:
			self.languages = set()

		if os.path.exists(RESOURCES_SKILLS_PICKLE):
			self.skills = pickle.load(open(RESOURCES_SKILLS_PICKLE))
		else:
			self.skills = set()

	def dumpPickles(self):
		pickle.dump(self.colleges, open(RESOURCES_COLLEGES_PICKLE, 'wb'))
		pickle.dump(self.companies, open(RESOURCES_COMPANIES_PICKLE, 'wb'))
		pickle.dump(self.courses, open(RESOURCES_COURSES_PICKLE, 'wb'))
		pickle.dump(self.degrees, open(RESOURCES_DEGREES_PICKLE, 'wb'))
		pickle.dump(self.job_titles, open(RESOURCES_JOB_TITLES_PICKLE, 'wb'))
		pickle.dump(self.languages, open(RESOURCES_LANGUAGES_PICKLE, 'wb'))
		pickle.dump(self.skills, open(RESOURCES_SKILLS_PICKLE, 'wb'))

	def save(self, format='xml', file_name=RESOURCES_DATA_RDF):

		# saving rdf
		f = open(file_name, 'wb')
		print >> f, self.graph.serialize(format=format)
		f.close()

		self.dumpPickles()

	def close(self):
		self.degree_socket_handler.close()
		self.language_socket_handler.close()
		self.university_socket_handler.close()

	def saveAndClose(self):
		self.close()
		self.save()

	def graph_add(self, s, p, o):
		self.graph.add((s, p, o))

	def add(self, profile):
		person = BNode()
		self.graph_add(person, RDF.type, FOAF.Person)

		self.add_language_triple(profile, person)
		self.add_skill_triple(profile, person)
		self.add_education_triple(profile, person)
		self.add_experience_triple(profile, person)

	def add_language_triple(self, profile, person):
		for language in profile.language_list:
			language = self.language_helper(language)
			term = self.schema.get_term(language)

			# if this is the new language we encounter
			if language not in self.languages:
				self.graph_add(term, RDF.type, self.schema.Language)
				self.languages.add(language)

			self.graph_add(person, self.schema.language, term)

	def add_skill_triple(self, profile, person):
		for skill_dict in profile.skill_list:
			skill_name = skill_dict['skill'].lower()
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
				college = self.university_helper(college)
				term = self.schema.get_term(college)

				if college not in self.colleges:
					self.graph_add(term, RDF.type, self.schema.College)
					self.graph_add(term, RDFS.label, Literal(college, datatype=XSD.string))
					self.colleges.add(college)

				self.graph_add(education, self.schema.college, term)

			if 'major' in education_dict:
				course = education_dict['major']
				#todo: add course_name helper
				term = self.schema.get_term(course)

				if course not in self.courses:
					self.graph_add(term, RDF.type, self.schema.Course)
					self.graph_add(term, RDF.type, self.schema.Concept)
					self.colleges.add(course)

				self.graph_add(education, self.schema.major, term)

			if 'degree' in education_dict:
				degree = education_dict['degree'].encode('ascii', 'ignore')
				degree, level = self.degree_helper(degree)
				if degree:
					term = self.schema.get_term(degree)

					if degree not in self.degrees:
						self.graph_add(term, RDF.type, self.schema.Degree)
						self.graph_add(term, self.schema.level, Literal(level, datatype=XSD.interger))
						self.degrees.add(degree)

					self.graph_add(education, self.schema.degree, term)

			self.graph_add(person, self.schema.education, education)

	def add_experience_triple(self, profile, person):
		for experience in profile.experience_list:

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
					if experience['to']:
						if self.check_datetime_format(experience['to']):
							self.graph_add(term, self.schema.to_time, Literal(experience['to'], datatype=XSD.date))
						elif experience['to'].lower() == 'current' or experience['to'].upper() == 'now':
							self.graph_add(term, self.schema.to_time, Literal('now', datatype=XSD.string))
				except KeyError:
					pass

			if 'company_name' in experience:
				company_name = experience['company_name']
				company_name = self.company_name_helper(company_name)
				company = self.schema.get_term(company_name)

				self.graph_add(company, RDFS.label, Literal(company_name, datatype=XSD.string))

				# add city info
				for city in self.get_cities_by_company_name(company_name):
					self.graph_add(company, self.schema.city, self.schema.get_term(city))

				# we need to define this company
				if company_name not in self.companies:
					self.graph_add(company, RDF.type, self.schema.Organization)
					#todo: get city info of the company
					self.companies.add(company_name)

					# extra process required for
					if 'company_url' in experience:
						company_profile = self.get_company_profile(experience['company_url'], company_name)

						if 'Founded' in company_profile:
							self.graph_add(company, self.schema.formation_year, Literal(company_profile['Founded'], datatype=XSD.gYear))

						if 'Company Size' in company_profile:
							mini, maxi = self.get_company_size(company_profile['Company Size'])
							self.graph_add(company, self.schema.from_value, Literal(mini, datatype=XSD.integer))
							self.graph_add(company, self.schema.to_time, Literal(maxi, datatype=XSD.integer))

						if 'Type' in company_profile:
							self.graph_add(company, self.schema.organization_type, Literal(company_profile['Type'], datatype=XSD.string))

						if 'Industry' in company_profile:
							self.graph_add(company, self.schema.industry, self.schema.get_term(company_profile['Industry']))

						DBHelper.dataSetRDF(company_profile['file_name'], rdf=1)

				self.graph_add(company, self.schema.has_position, term)
				self.graph_add(person, self.schema.works_as, term)

	def get_company_profile(self, url, company_name):
		file_path = CPD.downloadByUrl(url, company_name)
		parser = CPP(file_path)
		company_profile = parser.parseHtml().content
		DBHelper.dataAddEntry(company_profile['file_name'], url, exist=1, type='COMPANY')
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

	def language_helper(self, language):
		return self.language_socket_handler.send_query(language)

	def university_helper(self, university):
		return self.university_socket_handler.send_query(university)

	def degree_helper(self, degree):
		abbr, level = self.degree_socket_handler.send_query(degree)

		if not abbr:
			return None, None
		else:
			return abbr, int(level)

	def company_name_helper(self, company_name):
		return company_name.lower()

	def get_cities_by_company_name(self, company_name):
		cp = CityParser(company_name)
		return cp.getResult()
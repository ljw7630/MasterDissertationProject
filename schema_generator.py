from rdflib import Graph, URIRef, Literal
from rdflib.namespace import Namespace, NamespaceManager, FOAF, SKOS, XSD, RDF, RDFS, OWL
from html_parser import IndustryParser, DisciplineParser, DegreeAbbreviationParser


class SchemaGenerator:
	_base_uri = 'http://scss.tcd.ie/cs/muc/linkedin/'
	_owl_time_uri = 'http://www.w3.org/2006/time#'
	cities = ['Dublin', 'Galway', 'Cork', 'Limerick', 'Wexford']

	def __init__(self, uri=None):

		if uri is None:
			self._namespace_lk = Namespace(self._base_uri)
		else:
			self._namespace_lk = Namespace(uri)

		# self._namespace_time = Namespace(self._owl_time_uri)

		self.graph = Graph()
		# namespace_manager = NamespaceManager(self.graph)
		# namespace_manager.bind('lk', self._namespace_lk, override=True)
		#
		# # namespace_manager.bind('owl-time', self._owl_time_uri, override=False)
		# namespace_manager.bind('dbpedia-owl', Namespace('http://dbpedia.org/ontology/'), override=False)
		# namespace_manager.bind('aiiso', Namespace('http://purl.org/vocab/aiiso/schema#'), override=False)
		# self.graph.namespace_manager = namespace_manager
		self.graph.namespace_manager.reset()
		self.graph.namespace_manager.bind('lk', self._base_uri)
		self.graph.namespace_manager.bind('owl-time', Namespace(self._owl_time_uri))
		self.graph.namespace_manager.bind('dbpedia-owl', Namespace('http://dbpedia.org/ontology/'))
		self.graph.namespace_manager.bind('dbpedia', Namespace('http://dbpedia.org/property/'))
		self.graph.namespace_manager.bind('aiiso', Namespace('http://purl.org/vocab/aiiso/schema#'))
		self.graph.namespace_manager.bind('foaf', FOAF)
		self.graph.namespace_manager.bind('skos', SKOS)

		self.generate_class_definition()
		self.generate_property_definition()

	def generate_class_definition(self):
		# classes
		self.Concept = SKOS.Concept
		self.Person = FOAF.Person
		self.Organization = FOAF.Organization
		self.Position = self._namespace_lk.Position
		self.Speciality = self._namespace_lk.Speciality
		self.Skill = self._namespace_lk.Skill
		self.Industry = self._namespace_lk.Industry
		self.Language = URIRef('http://dbpedia.org/ontology/Language')
		self.City = URIRef('http://dbpedia.org/ontology/City')
		self.Education = self._namespace_lk.Education
		self.Course = URIRef('http://purl.org/vocab/aiiso/schema#Course')
		self.College = URIRef('http://purl.org/vocab/aiiso/schema#College')
		self.School = URIRef('http://purl.org/vocab/aiiso/schema#School')
		self.Degree = self._namespace_lk.Degree
		# define class
		self.graph.add((self.Position, RDF.type, OWL.Class))
		self.graph.add((self.Speciality, RDF.type, OWL.Class))
		self.graph.add((self.Skill, RDF.type, OWL.Class))
		self.graph.add((self.Industry, RDF.type, OWL.Class))
		self.graph.add((self.Education, RDF.type, OWL.Class))

		# define class relationship
		# self.graph.add((self.Skill, RDF.type, self.Concept))
		# self.graph.add((self.Speciality, RDF.type, self.Concept))
		# self.graph.add((self.Industry, RDF.type, self.Concept))

	def generate_property_definition(self):
		# properties
		self.id = self._namespace_lk.id
		self.skill = self._namespace_lk.skill
		self.language = URIRef('http://dbpedia.org/ontology/language')
		self.works_as = self._namespace_lk['worksAs']
		self.city = URIRef('http://dbpedia.org/ontology/city')
		#self.headquarter = URIRef('http://dbpedia.org/ontology/headquarter')
		self.industry = URIRef('http://dbpedia.org/ontology/industry')
		self.formation_year = URIRef('http://dbpedia.org/ontology/formationYear')
		self.number_of_employees = URIRef('http://dbpedia.org/ontology/numberOfEmployees')
		self.occupation = URIRef('http://dbpedia.org/property/occupation')
		self.has_position = self._namespace_lk['hasPosition']
		self.organization_type = self._namespace_lk.organizationType
		self.speciality = self._namespace_lk.speciality
		self.education = self._namespace_lk.education
		self.major = self._namespace_lk.major
		self.degree = self._namespace_lk.degree
		self.level = self._namespace_lk.level
		self.college = self._namespace_lk.college
		self.school = self._namespace_lk.school
		self.to_time = self._namespace_lk['to']
		self.from_value = self._namespace_lk['from']

		# define property
		self.graph.add((self.id, RDF.type,  OWL.DatatypeProperty))
		self.graph.add((self.skill, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.works_as, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.education, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.degree, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.college, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.school, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.to_time, RDF.type, OWL.DatatypeProperty))
		self.graph.add((self.from_value, RDF.type, OWL.DatatypeProperty))
		self.graph.add((self.has_position, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.organization_type, RDF.type, OWL.DatatypeProperty))
		self.graph.add((self.speciality, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.major, RDF.type, OWL.ObjectProperty))

		# define property domain and range
		self.graph.add((self.id, RDFS.domain, self.Person))
		self.graph.add((self.id, RDFS.range, XSD.string))
		self.graph.add((self.skill, RDFS.domain, self.Person))
		self.graph.add((self.skill, RDFS.range, self.Skill))
		self.graph.add((self.education, RDFS.domain, self.Person))
		self.graph.add((self.education, RDFS.range, self.Education))
		self.graph.add((self.major, RDFS.domain, self.Education))
		self.graph.add((self.major, RDFS.range, self.Course))
		self.graph.add((self.degree, RDFS.domain, self.Education))
		self.graph.add((self.degree, RDFS.range, self.Degree))
		self.graph.add((self.level, RDFS.domain, self.Degree))
		self.graph.add((self.level, RDFS.range, XSD.integer))
		self.graph.add((self.college, RDFS.domain, self.Education))
		self.graph.add((self.college, RDFS.range, self.College))
		self.graph.add((self.school, RDFS.domain, self.Education))
		self.graph.add((self.school, RDFS.range, self.School))
		self.graph.add((self.speciality, RDFS.domain, self.Organization))
		self.graph.add((self.speciality, RDFS.range, self.Organization))
		self.graph.add((self.works_as, RDFS.domain, self.Person))
		self.graph.add((self.works_as, RDFS.range, self.Position))
		self.graph.add((self.has_position, RDFS.domain, self.Organization))
		self.graph.add((self.has_position, RDFS.range, self.Position))
		self.graph.add((self.organization_type, RDFS.domain, self.Organization))
		self.graph.add((self.organization_type, RDFS.range, XSD.string))

	def generate_instance_discipline_hierarchy(self):
		disciplines = DisciplineParser().getDisciplinesHierarchy()

		self.generate_instance_discipline_hierarchy_helper(disciplines.keys(), disciplines)

	def generate_instance_discipline_hierarchy_helper(self, super_classes, dictionary):
		if super_classes == {}:
			return
		for super_class in super_classes:
			super_class_term = self.get_term(super_class)
			self.graph.add((super_class_term, RDF.type, self.Course))
			self.graph.add((super_class_term, RDF.type, SKOS.Concept))
			self.graph.add((super_class_term, SKOS.prefLabel, Literal(super_class, datatype=XSD.string)))
			for sub_class in dictionary[super_class].keys():

				self.graph.add((self.get_term(sub_class), SKOS.narrower, super_class_term))
				self.graph.add((super_class_term, SKOS.broader, self.get_term(sub_class)))

				self.generate_instance_discipline_hierarchy_helper(dictionary[super_class][sub_class].keys(),
					dictionary[super_class][sub_class])

	def generate_instance_industry(self):
		industries = IndustryParser().getIndustries()

		for industry in industries:
			self.graph.add((self.get_term(industry), RDF.type, self.Industry))
			self.graph.add((self.get_term(industry), RDFS.label, Literal(industry, datatype=XSD.date)))

	def generate_instance_degree(self):
		for degreeArr in DegreeAbbreviationParser().degrees:
			degreeAbbr = degreeArr[1]
			self.graph.add((self.get_term(degreeAbbr), RDF.type, SKOS.Concept))
			self.graph.add((self.get_term(degreeAbbr), SKOS.prefLabel, Literal(degreeArr[-1], datatype=XSD.string)))

	def generate_instance_city(self):
		for city in self.cities:
			self.graph.add((self.get_term(city), RDF.type, self.City))
			self.graph.add((self.get_term(city), RDFS.label, Literal(city, datatype=XSD.string)))

	def generate(self):

		self.generate_instance_industry()

		self.generate_instance_discipline_hierarchy()

		self.generate_instance_degree()

		self.generate_instance_city()

		return self.graph

	def get_term(self, term):
		return self._namespace_lk[term.replace(' ', '_')]

	def save(self, format='xml', file_name='result/ontology.owl'):
		f = open(file_name, 'w')
		print >> f, self.graph.serialize(format=format)
		f.close()


if __name__ == "__main__":
	sg = SchemaGenerator()
	sg.generate()
	sg.save(format='xml')
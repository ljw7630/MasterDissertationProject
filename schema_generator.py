from rdflib import Graph, URIRef
from rdflib.namespace import Namespace, NamespaceManager, FOAF, SKOS, XSD, RDF, RDFS, OWL


class SchemaGenerator:
	_base_uri = 'http://scss.tcd.ie/cs/muc/linkedin/'

	def __init__(self, uri=None):

		if uri is None:
			self._namespace_lk = Namespace(self._base_uri)
		else:
			self._namespace_lk = Namespace(uri)

		self.graph = Graph()
		namespace_manager = NamespaceManager(self.graph)
		namespace_manager.bind('lk', self._namespace_lk, override=False)

		self.graph.namespace_manager = namespace_manager
		self.graph.bind('foaf', FOAF)
		self.graph.bind('skos', SKOS)

	def generate(self):
		self.Concept = SKOS.Concept

		# classes
		self.Person = FOAF.Person
		self.Organization = FOAF.Organization
		self.Position = self._namespace_lk.Position
		self.Speciality = self._namespace_lk.Speciality
		self.Skill = self._namespace_lk.Skill
		self.Industry = self._namespace_lk.Industry
		self.Language = URIRef('http://dbpedia.org/ontology/Language')
		self.City = URIRef('http://dbpedia.org/ontology/City')
		self.Education = self._namespace_lk.Education
		self.Degree = self._namespace_lk.Degree
		self.Course = URIRef('http://purl.org/vocab/aiiso/schema#Course')
		self.College = URIRef('http://purl.org/vocab/aiiso/schema#College')
		self.School = URIRef('http://purl.org/vocab/aiiso/schema#School')

		# properties
		self.id = self._namespace_lk.id
		self.skill = self._namespace_lk.skill
		self.language = URIRef('http://dbpedia.org/ontology/language')
		self.works_as = self._namespace_lk['worksAs']
		self.city = URIRef('http://dbpedia.org/ontology/city')
		self.headquarter = URIRef('http://dbpedia.org/ontology/headquarter')
		self.industry = URIRef('http://dbpedia.org/ontology/industry')
		self.formation_year = URIRef('http://dbpedia.org/ontology/formationYear')
		self.number_of_employees = URIRef('http://dbpedia.org/ontology/numberOfEmployees')
		self.occupation = URIRef('http://dbpedia.org/property/occupation')
		self.has_position = self._namespace_lk['hasPosition']
		self.organization_type = self._namespace_lk.organizationType
		self.speciality = self._namespace_lk.speciality
		self.education = self._namespace_lk.education
		self.degree = self._namespace_lk.degree
		self.level = self._namespace_lk.level
		self.college = self._namespace_lk.college
		self.school = self._namespace_lk.school
		self.to_time = self._namespace_lk['to']
		self.from_time = self._namespace_lk['from']

		# define class
		self.graph.add((self.Position, RDF.type, OWL.Class))
		self.graph.add((self.Speciality, RDF.type, OWL.Class))
		self.graph.add((self.Skill, RDF.type, OWL.Class))
		self.graph.add((self.Industry, RDF.type, OWL.Class))
		self.graph.add((self.Education, RDF.type, OWL.Class))
		self.graph.add((self.Degree, RDF.type, OWL.Class))

		# define class relationship
		self.graph.add((self.Degree, RDF.type, self.Course))
		self.graph.add((self.Degree, RDF.type, self.Concept))
		self.graph.add((self.Skill, RDF.type, self.Concept))
		self.graph.add((self.Speciality, RDF.type, self.Concept))
		self.graph.add((self.Industry, RDF.type, self.Concept))

		# define property
		self.graph.add((self.id, RDF.type,  OWL.DataProperty))
		self.graph.add((self.skill, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.education, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.degree, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.college, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.school, RDF.type, OWL.ObjectProperty))
		self.graph.add((self.to_time, RDF.type, OWL.DataProperty))
		self.graph.add((self.from_time, RDF.type, OWL.DataProperty))
		self.graph.add((self.organization_type, RDF.type, OWL.DataProperty))
		self.graph.add((self.speciality, RDF.type, OWL.ObjectProperty))

		# define property domain and range
		self.graph.add((self.id, RDFS.domain, self.Person))
		self.graph.add((self.id, RDFS.range, XSD.string))
		self.graph.add((self.skill, RDFS.domain, self.Person))
		self.graph.add((self.skill, RDFS.range, self.Skill))
		self.graph.add((self.education, RDFS.domain, self.Person))
		self.graph.add((self.education, RDFS.range, self.Education))
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

		self.graph.close()

	def saveAtFile(self, format='turtle', file_name='result/ontology.owl'):
		f = open(file_name, 'w')
		print >> f, self.graph.serialize(format=format)
		f.close()
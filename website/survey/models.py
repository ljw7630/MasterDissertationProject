from django.db import models
from django.forms import ModelForm


DEGREE_CHOICES = (
('BOptom', 'Bachelor_in_Clinical_Optometry'),
('BAcc', 'Bachelor_of_Accounting'),
('BAppSc', 'Bachelor_of_Applied_Science'),
('BArch', 'Bachelor_of_Architecture'),
('BA', 'Bachelor_of_Arts'),
('BAE', 'Bachelor_of_Arts_and_Economics'),
('BASc', 'Bachelor_of_Arts_and_Science'),
('BMedSc', 'Bachelor_of_Biomedical_science'),
('BBA', 'Bachelor_of_Business_Administration'),
('BCL', 'Bachelor_of_Civil_Law'),
('BCoun', 'Bachelor_of_Counseling'),
('BCJ', 'Bachelor_of_Criminal_Justice'),
('BDS', 'Bachelor_of_Dental_Surgery'),
('BDes', 'Bachelor_of_Design'),
('BD', 'Bachelor_of_Divinity'),
('BScEcon', 'Bachelor_of_Economic_and_Social_Studies'),
('BEcon', 'Bachelor_of_Economics'),
('BEcon&Fin', 'Bachelor_of_Economics_and_Finance'),
('BEd', 'Bachelor_of_Education'),
('BEng', 'Bachelor_of_Engineering'),
('BFin', 'Bachelor_of_Finance'),
('BFA', 'Bachelor_of_Fine_Art'),
('BHSc', 'Bachelor_of_Health_Science'),
('LLB', 'Bachelor_of_Laws'),
('BLitt', 'Bachelor_of_Literature_or_Bachelor_of_Letters'),
('BMSc', 'Bachelor_of_Medical_Science'),
('MB', 'Bachelor_of_Medicine'),
('BMid', 'Bachelor_of_Midwifery'),
('BMin', 'Bachelor_of_Ministry'),
('BMus', 'Bachelor_of_Music'),
('BNurs', 'Bachelor_of_Nursing'),
('BPharm', 'Bachelor_of_Pharmacy'),
('BPhil', 'Bachelor_of_Philosophy'),
('BPhys', 'Bachelor_of_Physics'),
('BSc', 'Bachelor_of_Science'),
('BSc(Econ)', 'Bachelor_of_Science_in_Economics'),
('BSc(Eng)', 'Bachelor_of_Science_in_Engineering'),
('BSc(Psych)', 'Bachelor_of_Science_in_Psychology'),
('BSocSc', 'Bachelor_of_Social_Science'),
('BS', 'Bachelor_of_Surgery'),
('BTchg', 'Bachelor_of_Teaching'),
('BTech', 'Bachelor_of_Technology'),
('BTh', 'Bachelor_of_Theology'),
('BVMedSc', 'Bachelor_of_Veterinary_(Medical)_Science'),
('BVetMed', 'Bachelor_of_Veterinary_Medicine_(&_Surgery)'),
('DBA', 'Doctor_of_Business_Administration'),
('DCL', 'Doctor_of_Civil_Law_especially_at_Oxford'),
('DClinPsych', 'Doctor_of_Clinical_Psychology'),
('DDS', 'Doctor_of_Dental_Surgery'),
('DD', 'Doctor_of_Divinity'),
('EdD', 'Doctor_of_Education'),
('EdPsychD', 'Doctor_of_Educational_Psychology'),
('EngD', 'Doctor_of_Engineering'),
('HScD', 'Doctor_of_Health_Science'),
('LLD', 'Doctor_of_Laws'),
('DLitt', 'Doctor_of_Literature'),
('MD', 'Doctor_of_Medicine'),
('DMin', 'Doctor_of_Ministry'),
('DMus', 'Doctor_of_Music'),
('DNursSc', 'Doctor_of_Nursing_Science'),
('PhD', 'Doctor_of_Philosophy'),
('DPT', 'Doctor_of_Practical_Theology'),
('DProf', 'Doctor_of_Professional_Studies'),
('DSc', 'Doctor_of_Science'),
('SocScD', 'Doctor_of_Social_Science'),
('ThD', 'Doctor_of_Theology'),
('DUniv', 'Doctor_of_the_University'),
('MSc', 'Integrated_Master_in_Science'),
('JD', 'Juris_Doctor,_Juris_Doctorate,_Doctor_of_Jurisprudence'),
('Master', 'Master'),
('MOptom', 'Master_in_Clinical_Optometry'),
('MSc', 'Master_in_Science_(Master_of_Natural_Science_at_Cambridge_University)'),
('MAcc', 'Master_of_Accountancy'),
('MArch', 'Master_of_Architecture'),
('MA', 'Master_of_Arts'),
('MBiochem', 'Master_of_Biochemistry'),
('MBiolSc', 'Master_of_Biological_Science'),
('MBiol', 'Master_of_Biology'),
('MBA', 'Master_of_Business_Administration'),
('MBM', 'Master_of_Business_and_Management'),
('MChemPhys', 'Master_of_Chemical_Physics'),
('MChem', 'Master_of_Chemistry'),
('MCD', 'Master_of_Civic_Design'),
('MClinDent', 'Master_of_Clinical_Dentistry'),
('MMathComp', 'Master_of_Computational_Mathematics'),
('MComp', 'Master_of_Computing'),
('MDes', 'Master_of_Design'),
('MDiv', 'Master_of_Divinity'),
('MDrama', 'Master_of_Drama'),
('MEarthSci', 'Master_of_Earth_Science'),
('MEcon', 'Master_of_Economics'),
('MEd', 'Master_of_Education'),
('MEng', 'Master_of_Engineering'),
('MEnvSc', 'Master_of_Environmental_Science'),
('MFA', 'Master_of_Fine_Art'),
('MGeog', 'Master_of_Geography'),
('MGeol', 'Master_of_Geology'),
('MGeophys', 'Master_of_Geophysics'),
('MGeoscience', 'Master_of_Geoscience'),
('MInf', 'Master_of_Informatics'),
('MJur', 'Master_of_Jurisprudence_(Law)_(Magister_Juris_at_Oxford)'),
('LLM', 'Master_of_Laws'),
('MLitt', 'Master_of_Letters'),
('MLib', 'Master_of_Librarianship'),
('MMS', 'Master_of_Management_Studies'),
('MMath', 'Master_of_Mathematics'),
('MMORSE', 'Master_of_Mathematics,_Operational_Research,_Statistics_and_Economics'),
('MMathPhys', 'Master_of_Mathematics_and_Physics,_Master_of_Mathematical_Physics'),
('MMathStat', 'Master_of_Mathematics_and_Statistics'),
('MMus', 'Master_of_Music'),
('MNatSc', 'Master_of_Natural_Science'),
('MNursSc', 'Master_of_Nursing_Science'),
('MOcean', 'Master_of_Oceanography'),
('MPharm', 'Master_of_Pharmacy'),
('MPhil', 'Master_of_Philosophy'),
('MPhys', 'Master_of_Physics'),
('MPlan', 'Master_of_Planning'),
('MPS', 'Master_of_Professional_Studies'),
('MPA', 'Master_of_Public_Administration'),
('MPH', 'Master_of_Public_Health'),
('MRes', 'Master_of_Research'),
('MSc', 'Master_of_Science'),
('MSSc', 'Master_of_Social_Science'),
('MStat', 'Master_of_Statistics'),
('MSt', 'Master_of_Studies'),
('MTL', 'Master_of_Teaching_and_Learning'),
('MTheol', 'Master_of_Theology'),
('MUniv', 'Master_of_the_University'),
('PG_Dip', 'Postgraduate_Diploma'),
)

SCORE_CHOICES = (
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
)


# Create your models here.
class User(models.Model):
	name = models.CharField(null=True, max_length=50, blank=True)
	group = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return 'user: ' + str(self.id) + ', username: ' + self.name + ', group: ' + str(self.group)


class Answer(models.Model):
	user = models.ForeignKey(User)
	file = models.FilePathField()
	overall_score = models.IntegerField(null=True, blank=True, choices=SCORE_CHOICES)
	language_score = models.IntegerField(null=True, blank=True, choices=SCORE_CHOICES)
	skill_score = models.IntegerField(null=True, blank=True, choices=SCORE_CHOICES)

	city = models.CharField(max_length=20, null=True, blank=True)
	parse_city = models.CharField(max_length=20, null=True, blank=True)
	city_score = models.IntegerField(null=True, blank=True, choices=SCORE_CHOICES)

	def __unicode__(self):
		return 'user: ' + str(self.user.id) + ', answer: ' + str(self.id) + ', file: ' + self.file


class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['overall_score', 'language_score', 'skill_score', 'city', 'parse_city', 'city_score']


class Experience(models.Model):
	answer = models.ForeignKey(Answer)

	company = models.CharField(max_length=100, null=True, blank=True)
	job_title = models.CharField(max_length=100, null=True, blank=True)
	date_from = models.CharField(max_length=100, null=True, blank=True)
	date_to = models.CharField(max_length=100, null=True, blank=True)

	parse_company = models.CharField(max_length=100, null=True, blank=True)
	parse_job_title = models.CharField(max_length=100, null=True, blank=True)
	parse_date_from = models.CharField(max_length=100, null=True, blank=True)
	parse_date_to = models.CharField(max_length=100, null=True, blank=True)

	parse_score = models.IntegerField(null=True, blank=True, choices=SCORE_CHOICES)


class ExperienceForm(ModelForm):
	class Meta:
		model = Experience
		fields = ['company', 'job_title', 'date_from', 'date_to', 'parse_company', 'parse_job_title', 'parse_date_from',
		          'parse_date_to', 'parse_score']
		exclude=('answer')


class Education(models.Model):
	answer = models.ForeignKey(Answer)

	college = models.CharField(max_length=100, null=True, blank=True)
	major = models.CharField(max_length=100, null=True, blank=True)
	degree = models.CharField(max_length=100, null=True, blank=True, choices=DEGREE_CHOICES)
	date_from = models.CharField(max_length=100, null=True, blank=True)
	date_to = models.CharField(max_length=100, null=True, blank=True)

	parse_college = models.CharField(max_length=100, null=True, blank=True)
	parse_major = models.CharField(max_length=100, null=True, blank=True)
	parse_degree = models.CharField(max_length=100, null=True, blank=True, choices=DEGREE_CHOICES)
	parse_date_from = models.CharField(max_length=100, null=True, blank=True)
	parse_date_to = models.CharField(max_length=100, null=True, blank=True)

	parse_score = models.IntegerField(null=True, blank=True, choices=SCORE_CHOICES)


class EducationForm(ModelForm):
	class Meta:
		model = Education
		fields = ['college', 'major', 'degree', 'date_from', 'date_to', 'parse_college', 'parse_major', 'parse_degree',
		          'parse_date_from', 'parse_date_to', 'parse_score']
		exclude = ('answer')


class Language(models.Model):
	answer = models.ForeignKey(Answer)
	language = models.CharField(max_length=100, null=True, blank=True)
	parse_language = models.CharField(max_length=100, null=True, blank=True)


class LanguageForm(ModelForm):
	class Meta:
		model = Language
		fields = ['language']
		exclude = ('answer')


class Skill(models.Model):
	answer = models.ForeignKey(Answer)
	skill = models.CharField(max_length=100, null=True, blank=True)
	parse_skill = models.CharField(max_length=100, null=True, blank=True)


class SkillForm(ModelForm):
	class Meta:
		model = Skill
		fields = ['skill']
		exclude = ('answer')

# class Triple(models.Model):
# 	subject = models.CharField(max_length=100, null=True, blank=True)
# 	predicate = models.CharField(max_length=30, null=True, blank=True)
# 	object = models.CharField(max_length=100, null=True, blank=True)
#
# 	parse_subject = models.CharField(max_length=100, null=True, blank=True)
# 	parse_predicate = models.CharField(max_length=30, null=True, blank=True)
# 	parse_object = models.CharField(max_length=100, null=True, blank=True)
#
# 	score = models.IntegerField(null=True, blank=True)
#
# 	answer = models.ForeignKey(Answer)
#
# 	def __unicode__(self):
# 		return 'answer: ' + str(self.answer.id) + ', triple: ' + str(self.id)


class Data(models.Model):
	file_name = models.CharField(max_length=100, unique=True)
	user_group = models.IntegerField(null=True, blank=True)
	file_exists = models.BooleanField(default=False)
	file_url = models.CharField(max_length=150)
	rdf = models.BooleanField(default=0)
	type = models.CharField(default='PERSON', max_length=10)

	def __unicode__(self):
		return "data: " + self.file_name
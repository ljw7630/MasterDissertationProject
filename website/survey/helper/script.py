from glob import glob
from django.conf import settings
from random import choice
from survey.models import *
from survey.helper.survey_profile_cleaner import SurveyProfileCleaner
from html_parser import PublicProfileParser
from survey.helper.survey_rdf_generator import SurveyRDFGenerator


def generate_answer():
	files = set()
	all_profiles = glob(settings.TEMPLATE_PATH + '/*.htm')
	for g in range(settings.NUM_GROUPS):
		for i in range(settings.NUM_FILES):
			while True:
				profile_with_full_path = choice(all_profiles)
				profile = profile_with_full_path.rsplit('/', 1)[-1]
				if profile not in files:
					cleaner = SurveyProfileCleaner(profile_with_full_path)
					cleaner.saveToFile()
					files.add(profile)
					answer = Answer(file=profile)
					answer.save()
					break
		answers = Answer.objects.all().order_by('-id')[:settings.NUM_FILES]
		for i in reversed(answers):
			answer = Answer(file=i.file)
			answer.save()


def generate_data():
	generator = SurveyRDFGenerator()
	for g in range(settings.NUM_GROUPS):
		print 'The ', g, 'group'
		for i in range(1, settings.NUM_FILES+1):
			id1 = g * (settings.NUM_FILES * 2) + i
			id2 = id1 + settings.NUM_FILES
			answer1 = Answer.objects.get(pk=id1)
			answer2 = Answer.objects.get(pk=id2)

			path = answer1.file

			full_path = settings.TEMPLATE_PATH + '/' + path

			profile = PublicProfileParser(full_path).parseHtml()
			generator.add(profile)
			result = generator.get_result()

			answer1.parse_city = result.city
			answer2.parse_city = result.city

			answer1.save()
			answer2.save()

			fill_experience(answer1, result.experience_list)
			fill_education(answer1, result.education_list)
			fill_language(answer1, result.language_list)

			fill_experience(answer2, result.experience_list)
			fill_education(answer2, result.education_list)
			fill_language(answer2, result.language_list)
	generator.close()


def fill_experience(answer, experience_list):
	for experience in experience_list:
		exp = Experience(answer=answer)
		exp.company = ''
		if 'company' in experience:
			exp.parse_company = experience['company']
		exp.job_title = ''
		if 'job_title' in experience:
			exp.parse_job_title = experience['job_title']
		exp.date_from = ''
		if 'from' in experience:
			exp.parse_date_from = experience['from']
		exp.date_to = ''
		if 'to' in experience:
			exp.parse_date_to = experience['to']
		exp.answer = answer
		exp.save()

		print 'exp', exp.answer_id


def fill_education(answer, education_list):
	for education in education_list:
		edu = Education(answer=answer)
		edu.college = ''
		if 'college' in education:
			edu.parse_college = education['college']
		edu.major = ''
		if 'major' in education:
			edu.parse_major = education['major']
		edu.degree = ''
		if 'degree' in education:
			edu.parse_degree = education['degree']
		edu.date_from = ''
		if 'from' in education:
			edu.parse_date_from = education['from']
		edu.date_to = ''
		if 'to' in education:
			edu.parse_date_to = education['to']
		edu.answer = answer
		edu.save()

		print 'edu', edu.answer_id


def fill_language(answer, language_list):
	for language in language_list:
		lan = Language(answer=answer)
		lan.parse_language = language
		lan.answer = answer
		lan.save()

		print 'lan', lan.answer_id
from django.forms.models import modelformset_factory
from survey.models import *


class Storage:
	@staticmethod
	def insertExperiences(experience_list):
		pass

	@staticmethod
	def insertEducation(education_list):
		pass

	@staticmethod
	def insertLanguage(language_list):
		pass

	@staticmethod
	def insertSkill(skill_list):
		pass


# create new form
class FormHelper:

	@staticmethod
	def fillExperienceFormset(answer, formset, experience_list):
		print answer
		print experience_list
		idx = 0
		print 'list len', len(experience_list)
		print 'formset len', len(formset)
		for form in formset:
			experience = experience_list[idx]
			form.answer = answer
			print 'valid?', form.is_valid()
			print form.errors
			form = form.save(commit=False)
			if 'company' in experience:
				print 'company in experience'
				form.parse_company = experience['company']
			else:
				print 'company not in experience'
			if 'job_title' in experience:
				print 'job_title in experience'
				form.parse_job_title = experience['job_title']
			else:
				print 'job_title not in experience'
			if 'from' in experience:
				form.parse_date_from = experience['from']
			if 'to' in experience:
				form.parse_date_to = experience['to']

			form.answer = answer
			form.save()
			idx += 1

		ExperienceModelFormSet = modelformset_factory(Experience, extra=0)
		return ExperienceModelFormSet(queryset=Experience.objects.filter(answer_id=answer.id))

	@staticmethod
	def fillEducationFormset(answer, formset, education_list):
		print education_list
		idx = 0
		for form in formset:
			education = education_list[idx]
			form.answer = answer
			print 'valid?', form.is_valid()
			print form.errors
			form = form.save(commit=False)
			if 'college' in education:
				form.parse_college = education['college']
			if 'major' in education:
				form.parse_major = education['major']
			if 'degree' in education:
				form.parse_degree = education['degree']
			if 'from' in education:
				form.parse_date_from = education['from']
			if 'to' in education:
				form.parse_date_to = education['to']

			form.answer = answer
			form.save()
			idx += 1

		EducationModelFormSet = modelformset_factory(Education, extra=0)
		return EducationModelFormSet(queryset=Education.objects.filter(answer_id=answer.id))

	@staticmethod
	def fillLanguageFormset(answer, formset, language_list):
		idx = 0
		for form in formset:
			form = form.save(commit=False)
			form.parse_language = str(language_list[idx]).rsplit('/', 1)[-1]
			form.answer = answer
			form.save()
			idx += 1

		LanguageModelFormSet = modelformset_factory(Language, extra=0)
		return LanguageModelFormSet(queryset=Language.objects.filter(answer_id=answer.id))

	@staticmethod
	def fillSkillFormset(answer, formset, skill_list):
		idx = 0
		for form in formset:
			form = form.save(commit=False)
			form.parse_skill = str(skill_list[idx]).rsplit('/', 1)[-1]

			form.answer = answer
			form.save()
			idx += 1

		SkillModelFormSet = modelformset_factory(Skill, extra=0)
		return SkillModelFormSet(queryset=Skill.objects.filter(answer_id=answer.id))


	@staticmethod
	def fillAnswerForm(answer):
		form = AnswerForm(instance=answer, prefix='answer')
		return form
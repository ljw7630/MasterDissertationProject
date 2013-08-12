# Create your views here.

from django.shortcuts import render

from models import *
from django.http import HttpResponse, Http404
from django.conf import settings
from random import choice
from os.path import dirname
import os
from django.db.models import Max
from django.db.models import F
from glob import glob
from helper.survey_profile_cleaner import SurveyProfileCleaner
from helper.FormHelper import FormHelper
from helper.survey_rdf_generator import SurveyRDFGenerator
from html_parser import PublicProfileParser
import traceback
from django.forms.formsets import formset_factory


def print_users(request):
	user_list = User.objects.all()
	length = len(user_list)
	return render(request, 'users.html', {'user_list': user_list, 'length': length})


def print_form(request):
	# get user id, current file_id

	redirect = request.GET.get('redirect', 'false')
	print redirect
	try:
		if redirect == 'false':

			print 'GET', request.GET
			print 'POST', request.POST

			action_id = int(request.POST.get('action_id', '0'))

			# store the form base on action. render next action
			user_id = request.session['user_id']
			# action_id = request.session['action_id']
			print 'user_id:', user_id, 'action_id:', action_id
			if action_id % 2:
				answer = Answer.objects.filter(user_id=user_id).order_by('id')[action_id / 2]
				answer_form = AnswerForm(request.POST, instance=answer, prefix='answer')
				print 'valid answer?', answer_form.is_valid()
				print 'answer error?', answer_form.errors
				answer_form = answer_form.save(commit=False)
				answer_form.user_id = user_id
				answer_form.save()
			else:
				# store the rating to score model, render our next profile
				pass
			action_id += 1
			print 'user_id:', user_id, 'action_id:', action_id
		else:
			# first time user login
			name = request.GET.get('name', 'unknown')

			# calculate the group id for this user
			max_group_user = User.objects.filter(group__in=[User.objects.all().aggregate(Max('group'))['group__max']])
			cur_max_group_id = -1
			if max_group_user:
				cur_max_group_id = max_group_user[0].group
				if len(max_group_user) == 1:
					group = max_group_user[0].group
				else:
					group = max_group_user[0].group + 1
			else:
				group = 0
			new_user = User(name=name, group=group)
			new_user.save()

			print 'new_user', new_user

			# if this is a new group, generate random profiles
			# else get profiles from previous group user
			if group > cur_max_group_id:
				files = [f['file'] for f in Answer.objects.values('file')]
				cur_count = 0
				all_profiles = glob(settings.TEMPLATE_PATH + '/*.htm')
				while cur_count < settings.NUM_FILES:
					profile_with_full_path = choice(all_profiles)
					profile = profile_with_full_path.rsplit('/', 1)[-1]
					if profile not in files:
						cur_count += 1
						cleaner = SurveyProfileCleaner(profile_with_full_path)
						cleaner.saveToFile()
						answer = Answer(user_id=new_user.id, file=profile)
						files.append(profile)
						answer.save()
			else:
				same_group_answers = Answer.objects.filter(user__group=group)

				for f in same_group_answers.values('file'):
					a = Answer(user=new_user, file=f['file'])
					a.save()

			user_id = new_user.id
			action_id = 0

		request.session['user_id'] = user_id

		if action_id >= settings.NUM_FILES * 2:
			return render(request, 'thank_you.html')

		answer = Answer.objects.filter(user_id=user_id).order_by('id')[action_id / 2]
		path = answer.file
		full_path = settings.TEMPLATE_PATH + '/' + path
		profile = PublicProfileParser(full_path).parseHtml()

		if action_id % 2:
			if request.method == 'POST':
				ExperienceFormSet = formset_factory(ExperienceForm)
				EducationFormSet = formset_factory(EducationForm)
				LanguageFormSet = formset_factory(LanguageForm)
				experience_formset = ExperienceFormSet(request.POST, prefix='experience')
				education_formset = EducationFormSet(request.POST, prefix='education')
				language_formset = LanguageFormSet(request.POST, prefix='language')

				generator = SurveyRDFGenerator()
				generator.add(profile)
				result = generator.get_result()
				generator.close()

				answer.parse_city = result.city
				answer_form = FormHelper.fillAnswerForm(answer)

				experience_formset = FormHelper.fillExperienceFormset(answer, experience_formset, result.experience_list)
				education_formset = FormHelper.fillEducationFormset(answer, education_formset, profile.education_list)
				language_formset = FormHelper.fillLanguageFormset(answer, language_formset, profile.language_list)

			#render profile
				return render(request, 'compare.html', {'experience_formset': experience_formset
					, 'education_formset': education_formset, 'language_formset': language_formset
					, 'action_id': action_id, 'answer_form': answer_form})
		else:
			#render comparison

			ExperienceFormSet = formset_factory(ExperienceForm, extra=len(profile.experience_list))
			experience_formset = ExperienceFormSet(prefix='experience')
			EducationFormSet = formset_factory(EducationForm, extra=len(profile.education_list))
			education_formset = EducationFormSet(prefix='education')
			LanguageFormSet = formset_factory(LanguageForm, extra=len(profile.language_list))
			language_formset = LanguageFormSet(prefix='language')

			return render(request, 'survey.html', {'path': path, 'experience_formset': experience_formset
			, 'education_formset': education_formset, 'language_formset': language_formset, 'action_id': action_id})
	except:
		traceback.print_exc()
		# User.objects.get(id=user_id).delete()
		# Answer.objects.filter(user_id=user_id).delete()
		raise Http404

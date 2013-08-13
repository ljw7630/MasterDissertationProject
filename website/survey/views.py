# Create your views here.
from django.forms.models import modelformset_factory

from django.shortcuts import render

from models import *
from django.http import Http404
from django.conf import settings
from django.db.models import Max
from helper.form_helper import FormHelper
import traceback


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
			print 'user_id:', user_id, 'action_id:', action_id
			if action_id % 2:
				answer = Answer.objects.get(pk=(user_id-1) * settings.NUM_FILES + action_id/2 + 1)
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

			user_id = new_user.id
			action_id = 0

		request.session['user_id'] = user_id

		if action_id >= settings.NUM_FILES * 2:
			return render(request, 'thank_you.html')

		answer = Answer.objects.get(pk=(user_id - 1) * settings.NUM_FILES + action_id / 2 + 1)

		ExperienceFormSet = modelformset_factory(Experience, extra=0)
		EducationFormSet = modelformset_factory(Education, extra=0)
		LanguageFormSet = modelformset_factory(Language, extra=0)

		if action_id % 2:
			if request.method == 'POST':

				# experience
				experience_formset = ExperienceFormSet(request.POST, prefix='experience')
								# queryset=Experience.objects.filter(answer_id=answer.id))
				exps = Experience.objects.filter(answer=answer)
				idx = 0
				print 'len exp fs', len(experience_formset)
				for form in experience_formset:
					exps[idx].company = form['company']
					exps[idx].parse_company_score = form['parse_company_score']
					exps[idx].job_title = form['job_title']
					exps[idx].parse_job_title_score = form['parse_job_title_score']
					exps[idx].date_from = form['date_from']
					exps[idx].parse_date_from_score = form['parse_date_from_score']
					exps[idx].date_to = form['date_to']
					exps[idx].parse_date_to_score = form['parse_date_to_score']
					exps[idx].save()
					idx += 1

				experience_formset = ExperienceFormSet(prefix='experience',
						queryset=Experience.objects.filter(answer_id=answer.id))

				# if experience_formset.is_valid():
				# 	experience_formset.save()
				# else:
				# 	print experience_formset.errors

				# education
				education_formset = EducationFormSet(request.POST, prefix='education')
								# queryset=Education.objects.filter(answer_id=answer.id))
				print 'len edu fs', len(education_formset)
				edus = Education.objects.filter(answer=answer)
				idx = 0
				for form in education_formset:
					edus[idx].college = form['college']
					edus[idx].parse_college_score = form['parse_college_score']
					edus[idx].major = form['major']
					edus[idx].parse_major_score = form['parse_major_score']
					edus[idx].degree = form['degree']
					edus[idx].parse_degree_score = form['parse_degree_score']
					edus[idx].date_from = form['date_from']
					edus[idx].parse_date_from_score = form['parse_date_from_score']
					edus[idx].date_to = form['date_to']
					edus[idx].parse_date_to_score = form['parse_date_to_score']
					edus[idx].save()
					idx += 1

				education_formset = EducationFormSet(prefix='education',
						queryset=Education.objects.filter(answer_id=answer.id))

				# if education_formset.is_valid():
				# 	education_formset.save()
				# else:
				# 	print education_formset.save()

				language_formset = LanguageFormSet(request.POST, prefix='language')
								# queryset=Language.objects.filter(answer_id=answer.id))

				lans = Language.objects.filter(answer=answer)
				idx=0
				for form in language_formset:
					lans[idx].language = form['language']
					lans[idx].parse_language_score = form['parse_language_score']
					lans[idx].save()
					idx += 1

				language_formset = LanguageFormSet(prefix='language',
						queryset=Language.objects.filter(answer_id=answer.id))
				# if language_formset.is_valid():
				# 	language_formset.save()

				answer_form = FormHelper.fillAnswerForm(answer)

				#render profile
				return render(request, 'compare.html', {'experience_formset': experience_formset
				, 'education_formset': education_formset, 'language_formset': language_formset
				, 'action_id': action_id, 'answer_form': answer_form})
		else:
			#render survey
			path = answer.file

			experience_formset = ExperienceFormSet(queryset=Experience.objects.filter(answer_id=answer.id),
			                                       prefix='experience')
			education_formset = EducationFormSet(queryset=Education.objects.filter(answer_id=answer.id),
			                                     prefix='education')
			language_formset = LanguageFormSet(queryset=Language.objects.filter(answer_id=answer.id), prefix='language')

			return render(request, 'survey.html', {'path': path, 'experience_formset': experience_formset
			, 'education_formset': education_formset, 'language_formset': language_formset, 'action_id': action_id})
	except:
		traceback.print_exc()
		raise Http404

# Create your views here.
from django.forms.models import modelformset_factory

from django.shortcuts import render

from models import *
from django.http import Http404
from django.conf import settings
from django.db.models import Max
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
				answer = Answer.objects.get(pk=(user_id - 1) * settings.NUM_FILES + action_id / 2 + 1)
				answer_form = AnswerForm(request.POST, instance=answer, prefix='answer')
				print 'valid answer?', answer_form.is_valid()
				print 'answer error?', answer_form.errors
				answer_form = answer_form.save(commit=False)
				answer_form.user_id = user_id
				answer_form.save()

				# store score information
				ExperienceFormSet = modelformset_factory(Experience, extra=0)
				experience_formset = ExperienceFormSet(request.POST, prefix='experience',
														queryset=Experience.objects.filter(answer_id=answer.id))
				exps = Experience.objects.filter(answer=answer)
				idx = 0
				for form in experience_formset:
					item = exps[idx]
					if form['parse_company_score'].data:
						item.parse_company_score = int(form['parse_company_score'].data)

					if form['parse_job_title_score'].data:
						item.parse_job_title_score = int(form['parse_job_title_score'].data)

					if form['parse_date_from_score'].data:
						item.parse_date_from_score = int(form['parse_date_from_score'].data)

					if form['parse_date_to_score'].data:
						item.parse_date_to_score = int(form['parse_date_to_score'].data)

					item.save()
					idx += 1

				EducationFormSet = modelformset_factory(Education, extra=0)
				education_formset = EducationFormSet(request.POST, prefix='education',
														queryset=Education.objects.filter(answer_id=answer.id))
				edus = Education.objects.filter(answer=answer)
				idx = 0
				for form in education_formset:
					item = edus[idx]
					if form['parse_college_score'].data:
						item.parse_college_score = int(form['parse_college_score'].data)

					if form['parse_major_score'].data:
						item.parse_major_score = int(form['parse_major_score'].data)

					if form['parse_degree_score'].data:
						item.parse_degree_score = int(form['parse_degree_score'].data)

					if form['parse_date_from'].data:
						item.parse_date_from = int(form['parse_date_from'].data)

					if form['parse_date_to'].data:
						item.parse_date_to = int(form['parse_date_to'].data)

					item.save()
					idx += 1

				LanguageFormSet = modelformset_factory(Language, extra=0)
				language_formset = LanguageFormSet(request.POST, prefix='language',
													queryset=Language.objects.filter(answer_id=answer.id))
				lans = Language.objects.filter(answer=answer)
				idx = 0
				for form in language_formset:
					item = lans[idx]
					if form['parse_language_score'].data:
						item.parse_language_score = int(form['parse_language_score'].data)

					item.save()
					idx += 1
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
			if max_group_user:
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

		if action_id % 2:
			if request.method == 'POST':

				ExperienceFormSet = modelformset_factory(Experience)
				EducationFormSet = modelformset_factory(Education)
				LanguageFormSet = modelformset_factory(Language)

				# experience
				experience_formset = ExperienceFormSet(request.POST, prefix='experience',
													queryset=Experience.objects.filter(answer_id=answer.id))
				exps = Experience.objects.filter(answer=answer)
				idx = 0
				print 'len exp fs', len(experience_formset)
				for form in experience_formset:
					item = exps[idx]
					if form['company'].data:
						item.company = str(form['company'].data.encode('ascii', 'ignore'))
					if form['job_title'].data:
						item.job_title = str(form['job_title'].data.encode('ascii', 'ignore'))
					if form['date_from'].data:
						item.date_from = str(form['date_from'].data.encode('ascii', 'ignore'))
					if form['date_to'].data:
						item.date_to = str(form['date_to'].data.encode('ascii', 'ignore'))
					item.save()
					idx += 1

				ExperienceFormSet = modelformset_factory(Experience, extra=0)
				experience_formset = ExperienceFormSet(prefix='experience',
													queryset=Experience.objects.filter(answer_id=answer.id))

				# education
				education_formset = EducationFormSet(request.POST, prefix='education',
													queryset=Education.objects.filter(answer_id=answer.id))
				print 'len edu fs', len(education_formset)
				edus = Education.objects.filter(answer=answer)
				idx = 0
				for form in education_formset:
					item = edus[idx]
					if form['college'].data:
						item.college = str(form['college'].data.encode('ascii', 'ignore'))
					if form['major'].data:
						item.major = str(form['major'].data.encode('ascii', 'ignore'))
					if form['degree'].data:
						item.degree = str(form['degree'].data.encode('ascii', 'ignore'))
					if form['date_from'].data:
						item.date_from = str(form['date_from'].data.encode('ascii', 'ignore'))
					if form['date_to'].data:
						item.date_to = str(form['date_to'].data.encode('ascii', 'ignore'))
					item.save()
					idx += 1

				EducationFormSet = modelformset_factory(Education, extra=0)
				education_formset = EducationFormSet(prefix='education',
													queryset=Education.objects.filter(answer_id=answer.id))

				language_formset = LanguageFormSet(request.POST, prefix='language',
													queryset=Language.objects.filter(answer_id=answer.id))

				lans = Language.objects.filter(answer=answer)
				idx = 0
				for form in language_formset:
					item = lans[idx]
					if form['language'].data:
						item.language = str(form['language'].data.encode('ascii', 'ignore'))
					item.save()
					idx += 1

				LanguageFormSet = modelformset_factory(Language, extra=0)
				language_formset = LanguageFormSet(prefix='language',
													queryset=Language.objects.filter(answer_id=answer.id))

				answer_form = AnswerForm(request.POST, instance=answer, prefix='answer')

				answer.city = str(answer_form['city'].data.encode('ascii', 'ignore'))
				answer.save()
				answer_form = AnswerForm(instance=answer, prefix='answer')

				#render profile
				return render(request, 'compare.html', {'experience_formset': experience_formset
				, 'education_formset': education_formset, 'language_formset': language_formset
				, 'action_id': action_id, 'answer_form': answer_form})
		else:
			path = answer.file

			answer_form = AnswerForm(instance=answer, prefix='answer')

			ExperienceFormSet = modelformset_factory(Experience, extra=0)
			EducationFormSet = modelformset_factory(Education, extra=0)
			LanguageFormSet = modelformset_factory(Language, extra=0)

			experience_formset = ExperienceFormSet(queryset=Experience.objects.filter(answer_id=answer.id),
												prefix='experience')
			education_formset = EducationFormSet(queryset=Education.objects.filter(answer_id=answer.id),
												prefix='education')
			language_formset = LanguageFormSet(queryset=Language.objects.filter(answer_id=answer.id), prefix='language')

			return render(request, 'survey.html', {'path': path, 'experience_formset': experience_formset
			, 'education_formset': education_formset, 'language_formset': language_formset, 'answer_form': answer_form,
						'action_id': action_id})
	except:
		traceback.print_exc()
		raise Http404

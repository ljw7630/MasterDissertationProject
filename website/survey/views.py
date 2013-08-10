# Create your views here.

from django.shortcuts import render

from models import User, Answer
from forms import TripleForm
from django.http import HttpResponse, Http404
from django.conf import settings
from random import choice
from os.path import dirname
import os
from django.db.models import Max
from django.db.models import F


def print_users(request):
	user_list = User.objects.all()
	length = len(user_list)
	return render(request, 'users.html', {'user_list': user_list, 'length': length})


def print_form(request):
	# get user id, current file_id

	redirect = request.GET.get('redirect', 'false')
	print redirect
	if redirect == 'false':
		# store the form base on action. render next action
		user_id = request.session['user_id']
		action_id = request.session['action_id']
		print 'user_id:', user_id, 'action_id:', action_id
		if action_id % 2:
			# store the item to Triple model, and render our auto generated triples
			# to compare form
			pass
		else:
			# store the rating to score model, render our next profile
			pass
		action_id += 1
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

		# if this is a new group, generate random profiles
		# else get profiles from previous group user
		if group > cur_max_group_id:
			files = Answer.objects.values('file')
			cur_count = 0
			all_profiles = os.listdir(settings.TEMPLATE_PATH)
			while cur_count < settings.NUM_FILES:
				profile = choice(all_profiles)
				if profile not in files:
					cur_count += 1
					answer = Answer(user_id=new_user.id, file=profile)
					answer.save()
		else:
			same_group_answers = Answer.objects.filter(user__group=group)

			for f in same_group_answers.values('file'):
				a = Answer(user=new_user, file=f['file'])
				a.save()

		user_id = new_user.id
		action_id = 0

	request.session['user_id'] = user_id
	request.session['action_id'] = action_id
	if action_id % 2:
		#render profile
		return render(request, 'compare.html', compare(request))
	else:
		#render comparison
		path = 'lijinwu.htm'
		return render(request, 'survey.html', {'path': path,
		                                       'experiences': range(2),
		                                       'educations': range(3),
		                                       'skills': range(4)})

	# return HttpResponse(name)

	# path = 'lijinwu.htm'
	# form = TripleForm()

	# return render(request, 'survey.html',
	#               {'path': path,
	#                'experiences': range(2),
	#                'educations': range(3),
	#                'skills': range(4)})


def compare(request):
	city1 = 'Dublin'
	experiences1 = [{'company': 'McCann FitzGerald', 'job_title': 'Solicitor and Trade Mark Agent',
	                'from': '2004-09', 'to': 'now'}]
	education1 = [
		{'college': 'Trinity College, Dublin', 'degree': 'LLB', 'from': 1999, 'to': '2003'},
		{'college': 'Sutton Park School', 'from': 1993, 'to': 1999}]
	skills1 = ["Copyright Law", "E-commerce",
	           "Sports Law", "Confidentiality",
	           "Digital Rights", "Intellectual Property",
	           "Legal Advice", "Privacy Law", "Data Privacy", "Trademarks", "IT law", "Software Licensing",
	           "Sponsorship", "Outsourcing"]
	city2 = 'Dublin'
	experiences2 = [{'company': 'McCann_FitzGerald', 'job_title': 'Solicitor_and_Trade_Mark_Agent',
	                 'from': '2004-09'}]
	education2 = [
		{'college': 'Trinity_College_Dublin', 'degree': 'LLB', 'from': 1999, 'to': '2003'},
		{'college': 'Sutton_Park_School', 'from': 1993, 'to': 1999}]
	skills2 = ["Copyright Law", "E-commerce",
	           "Sports Law", "Confidentiality",
	           "Digital Rights", "Intellectual Property",
	           "Legal Advice", "Privacy Law", "Data Privacy", "Trademarks", "IT law", "Software Licensing",
	           "Sponsorship", "Outsourcing"]

	return {'city1': city1, 'city2': city2,
	        'experiences1': experiences1, 'experiences2': experiences2,
	        'education1': education1, 'education2': education2,
	        'skills1': skills1, 'skills2': skills2}

	# return render(request, 'compare.html',
	#               {'city1': city1,
	#                'city2': city2,
	#                'experiences1': experiences1,
	#                'experiences2': experiences2,
	#                'education1': education1,
	#                'education2': education2,
	#                'skills1': skills1,
	#                'skills2': skills2})
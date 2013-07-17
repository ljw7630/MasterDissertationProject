# Create your views here.

from django.shortcuts import render

from models import User
from forms import TripleForm


def print_users(request):
	user_list = User.objects.all()
	length = len(user_list)
	return render(request, 'users.html', {'user_list': user_list, 'length': length})


def print_form(request):
	path = 'adamdfinlay.htm'
	# form = TripleForm()

	return render(request, 'survey.html',
	              {'path': path,
	               'experiences': range(2),
	               'educations': range(3),
	               'skills': range(4)})


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
	return render(request, 'compare.html',
	              {'city1': city1,
	               'city2': city2,
	               'experiences1': experiences1,
	               'experiences2': experiences2,
	               'education1': education1,
	               'education2': education2,
	               'skills1': skills1,
	               'skills2': skills2})
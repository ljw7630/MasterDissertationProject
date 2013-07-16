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
	return render(request, 'compare.html',
		{'experiences': range(2),
		 'educations': range(3),
		 'skills': range(4)})
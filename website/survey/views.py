# Create your views here.
import os

from django.shortcuts import render

from models import User
from forms import TripleForm
import sys


def print_users(request):
	user_list = User.objects.all()
	length = len(user_list)
	return render(request, 'users.html', {'user_list': user_list, 'length': length})


def print_form(request):

	path = 'aaroncobrien.htm'
	form = TripleForm()

	return render(request, 'survey.html', {'path': path, 'survey_form': form})


def finish(request):
	return render(request, 'thank_you.html')
# Create your views here.
import os

from django.shortcuts import render

from models import User
from forms import TripleForm
from profile_cleaner import ProfileCleaner as PC


def print_users(request):
	user_list = User.objects.all()
	length = len(user_list)
	return render(request, 'users.html', {'user_list': user_list, 'length': length})


def print_form(request):

	cleaner = PC(os.path.realpath('../user_raw/lijinwu.htm'))
	path = cleaner.saveToFile()
	form = TripleForm()

	return render(request, 'survey.html', {'path': path, 'survey_form': form})


def finish(request):
	return render(request, 'thank_you.html')
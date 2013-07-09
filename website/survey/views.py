# Create your views here.
from models import User, Answer, Triple
from django.shortcuts import render
from forms import TripleForm
from helper.profile_cleaner import ProfileCleaner as PC
from django.template.loader import get_template


def print_users(request):
	user_list = User.objects.all()
	length = len(user_list)
	return render(request, 'users.html', {'user_list': user_list, 'length': length})


def print_form(request):

	cleaner = PC('/Users/jinwu/GitHub/MasterDissertationProject/user_raw/lijinwu.htm')
	path = cleaner.saveToFile()
	form = TripleForm()

	return render(request, 'survey.html', {'path': path, 'survey_form': form})


def finish(request):
	return render(request, 'thank_you.html')
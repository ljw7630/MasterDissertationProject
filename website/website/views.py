from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, Template
from django.template.loader import get_template
import datetime
from django.shortcuts import redirect


def consent(request):
	name = request.GET.get('name', 'unknown')
	if not name:
		return HttpResponse('Please type in your name.')

	return redirect('/survey/print_form/?name='+name+'&redirect=true')


def hello(request):
	t = get_template('consent_form.html')
	c = Context()
	return HttpResponse(t.render(c))
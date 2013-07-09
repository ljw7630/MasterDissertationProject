from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.template.loader import get_template
import datetime
from django.shortcuts import redirect


def consent(request):
	click = request.GET.get('btn', 'disagree')
	name = request.GET.get('name', 'unknown')

	if click == 'agree':
		return redirect('/print_form')
	else:
		raise Http404

	# t = Template('<p>{{click}}</p> <p>{{name}}</p>')
	# c = Context({'click': click, 'name': name})
	# return HttpResponse(t.render(c))


def hello(request):

	# hello_world = """
	# 	{% load compressed %}
	# 	<head>
	# 		{% compressed_css 'bootstrap' %}
	# 		{% compressed_js 'bootstrap' %}
	# 	</head>
	# 	<body>
	# 		<div class="container">
	# 			<div class="row">
	# 				<h1> Hello world</h1>
	# 			</div>
	# 		</div>
	# 	</body>"""
	# t = Template(hello_world)
	t = get_template('consent_form.html')
	c = Context()
	return HttpResponse(t.render(c))


def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)


def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)
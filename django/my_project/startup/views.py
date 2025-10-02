from django.http import HttpResponse
from django.template import loader
from .models import Member
import datetime

# def startup(request): return HttpResponse("Hello world!")

def main(request):
	template = loader.get_template('main.html')
	host = request.get_host()
	context = { 'timestamp': datetime.datetime.now().isoformat(), 'host': host }
	return HttpResponse(template.render(context))

def lister(request):
	startups = Member.objects.all().order_by('lastname', 'firstname').values()
	template = loader.get_template('lister.html')
	host = request.get_host()
	context = {'startups': startups, 'host': host }
	return HttpResponse(template.render(context, request))

def details(request, id):
	startups = Member.objects.get(id=id)
	template = loader.get_template('details.html')
	host = request.get_host()
	context = {'startups': startups, 'host': host }
	return HttpResponse(template.render(context, request))

def testing(request):
	template = loader.get_template('template.html')
	startups = Member.objects.all().order_by('lastname', 'firstname').values()
	host = request.get_host()
	context = {
		'letters': ['alpha', 'beta', 'gamma', 'delta'],
		'timestamp': datetime.datetime.now().isoformat(),
		'startups': startups,
		'host': host
	}
	return HttpResponse(template.render(context, request))

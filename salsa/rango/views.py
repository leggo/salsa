from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	context = RequestContext(request)
	context_dict = { 'boldmessage': "I am bold font from the context"}
	return render_to_response('rango/index.html', context_dict, context)
	
	
	
	#return HttpResponse("Halli, Hallo, Haalle! Here is a link to <a href='http://127.0.0.1:8000/rango/about/'>about</a> ")
	
def about(request):
	context = RequestContext(request)
	context_dict = { 'schlurp': "Hi, my name is Schlurp!"}
	return render_to_response('rango/about.html', context_dict, context)
	#return HttpResponse('Yes, this is abuut. And <a href="http://127.0.0.1:8000/rango/">here</a> is a link to the home page')
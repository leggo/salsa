from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page

def index(request):
	context = RequestContext(request)
	
	category_list = Category.objects.order_by('-likes')[:5]
	most_viewed_pages = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': most_viewed_pages}
	
	for category in category_list:
		category.url = category.name.replace(' ', '_')
	
	return render_to_response('rango/index.html', context_dict, context)
	
	
	
	#return HttpResponse("Halli, Hallo, Haalle! Here is a link to <a href='http://127.0.0.1:8000/rango/about/'>about</a> ")
	
def about(request):
	context = RequestContext(request)
	context_dict = { 'schlurp': "Hi, my name is Schlurp!"}
	return render_to_response('rango/about.html', context_dict, context)
	#return HttpResponse('Yes, this is abuut. And <a href="http://127.0.0.1:8000/rango/">here</a> is a link to the home page')
	
def category(request, category_name_url):

	context = RequestContext(request)
	
	category_name = category_name_url.replace('_', ' ')
	
	context_dict = {'category_name': category_name}
	
	try:
		
		category = Category.objects.get(name = category_name)
		
		pages = Page.objects.filter(category=category)
		
		context_dict['category'] = category
		
		context_dict['pages'] = pages
		
	except Category.DoesNotExist:
	
		pass
		
	return render_to_response('rango/category.html', context_dict, context)
		
	

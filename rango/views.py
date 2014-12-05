from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page
from rango.models import UserProfile
from rango.forms import CategoryForm 
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

def encode_url(str):
	return str.replace(' ', '_')


def decode_url(category_name_url):
	return category_name_url.replace('_', ' ')
	
	
	
def get_cat_list():
	
	cat_list = []
	cat_list = Category.objects.all()
	for category in cat_list:
		category.url = encode_url(category.name)
	
	return cat_list
	
	

def track_url(request):
	hello = 'no'
	context = RequestContext(request)
	if request.method == 'GET':
		if page_id in request.GET:
			hello = 'yes'
	return HttpResponse(hello)
	
def index(request):
	
	context = RequestContext(request)
	
	category_list = Category.objects.order_by('-views')[:4]
	context_dict = {'categories': category_list}
	

	context_dict['cat_list'] = get_cat_list()
	
	for category in category_list:
		category.url = encode_url(category.name)
	
#	page_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
#	context_dict = {'categories': category_list, 'pages': most_viewed_pages}
		


	
	if request.session.get('last_visit'):
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits', 0)
		
		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 5:
			request.session['visits'] = visits + 1
			request.session['last_visit'] = str(datetime.now())
			
	else:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1

	return render_to_response('rango/index.html', context_dict, context)
	
	#return HttpResponse("Halli, Hallo, Haalle! Here is a link to <a href='http://127.0.0.1:8000/rango/about/'>about</a> ")
	

	
def about(request):
	context = RequestContext(request)
	context_dict = { 'cat_list': get_cat_list() }

	if request.session.get('visits'):
		count = request.session.get('visits')
		time = request.session.get('last_visit')
	else:
		count = 0
		
	context_dict['visits'] = count
	context_dict['timer'] = time
		
		
	return render_to_response('rango/about.html', context_dict, context)
	
	#return HttpResponse('Yes, this is abuut. And <a href="http://127.0.0.1:8000/rango/">here</a> is a link to the home page')
	
def category(request, category_name_url):

	context = RequestContext(request)
	category_name = category_name_url.replace('_', ' ')
	result_list = []
	

	context_dict = {'category_name': category_name, 'category_name_url': category_name_url, 'cat_list': get_cat_list()}
	

	

	
	try:
		
		category = Category.objects.get(name = category_name)
		
		pages = Page.objects.filter(category=category)
		
		context_dict['category'] = category
		
		context_dict['pages'] = pages
		
		#context_dict['category_name_url'] = category_name_url
		
	except Category.DoesNotExist:
	
		pass
	
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	
			context_dict['result_list'] = result_list
		
	return render_to_response('rango/category.html', context_dict, context)
	

		
	
@login_required	
def add_category(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('rango/add_category.html', {'form': form, 'cat_list': get_cat_list()}, context)
	


@login_required	
def add_page(request, category_name_url):
	context = RequestContext(request)
	
	category_name = decode_url(category_name_url)
	
	if request.method == 'POST':
		form = PageForm(request.POST)
		
		if form.is_valid():
			page = form.save(commit=False)
			
			try:
				cat = Category.objects.get(name=category_name)
				page.category = cat
			except Category.DoesNotExist:
			
				return render_to_response('rango/add_category.html', {}, context)
				
				
			page.views = 0
			
			page.save()
			
			return category(request, category_name_url)
			
		else:
			print form.errors
	
	else:
		form = PageForm()
		
	return render_to_response('rango/add_page.html',
			{'category_name_url': category_name_url,
			'category_name': category_name, 'form': form, 
			'cat_list': get_cat_list()},
			context)
			
			
def register(request):

	context = RequestContext(request)
	
	registered = False
	
	if request.method == 'POST':
	
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
		
		else:
			print user_form.errors, profile_form.errors
			
	else:
		
		user_form = UserForm()
		profile_form = UserProfileForm()
		
		
	return render_to_response(
			'rango/register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
			'cat_list': get_cat_list()},
			context)
			
			
			
def user_login(request):
	
	
	context = RequestContext(request)
	context_dict = {}
	
	
	if request.method == 'POST':
		
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
				
			else:
				context_dict['disabled_account'] = True
				return render_to_response('rango/login.html', context_dict, context)
				
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			context_dict['bad_details'] = True
			return render_to_response('rango/login.html', context_dict, context)
			
	else:
		return render_to_response('rango/login.html', {'cat_list': get_cat_list()}, context)
	
	
@login_required	
def restricted(request):
		
		context = RequestContext(request)
		context_dict = {'cat_list': get_cat_list()}
		
		return render_to_response('rango/restricted.html', context_dict, context)
	
	
@login_required
def user_logout(request):

	logout(request)
	
	return HttpResponseRedirect('/rango/')
	
	
@login_required
def profile(request):
	context = RequestContext(request)

	try:
		myuser = UserProfile.objects.get(user=request.user)
	except:
		myuser = None
		
	mycontext = {'userprofile': myuser}	


	
	
	return render_to_response('rango/profile.html', mycontext, context)
	

	
	
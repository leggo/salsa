from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm 
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
	

	context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
	

	

	
	try:
		
		category = Category.objects.get(name = category_name)
		
		pages = Page.objects.filter(category=category)
		
		context_dict['category'] = category
		
		context_dict['pages'] = pages
		
		#context_dict['category_name_url'] = category_name_url
		
	except Category.DoesNotExist:
	
		pass
		
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
    return render_to_response('rango/add_category.html', {'form': form}, context)
	

def decode_url(category_name_url):
	return category_name_url.replace('_', ' ')
	
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
			'category_name': category_name, 'form': form},
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
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
			context)
			
			
			
def user_login(request):
	
	context = RequestContext(request)
	
	if request.method == 'POST':
		
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
				
			else:
				return HttpResponse("Your Rango account is disabled.")
				
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
			
	else:
		return render_to_response('rango/login.html', {}, context)
	
	
@login_required	
def restricted(request):
		return HttpResponse("Since you're logged in, you can see this text!")
	
	
@login_required
def user_logout(request):

	logout(request)
	
	return HttpResponseRedirect('/rango/')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
			
			
			
			
		

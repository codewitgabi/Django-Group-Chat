from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User , auth
from django.contrib import messages
from .models import Category, Group, Message
from django.db.models import Q, Count
from .forms import CustomUserCreationForm


def redirect_auth_user(func):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect("index")
		return func(request, *args, **kwargs)
	return wrapper
	

@login_required(login_url="signin")
def index(request):
	search = request.GET.get("search", "") # get search data
	query_param = request.GET.get("cat", "") # get category
	
	categories = Category.objects.all().annotate(
		num_groups=Count("group")
	).order_by("num_groups")
	
	groups = Group.objects.filter(
		Q(name__icontains=search) |
		Q(creator__username__icontains=search),
		category__name__icontains=query_param,
	).order_by("?")
	
	context = {
		"categories": categories,
		"groups": groups
	}
	return render(request, "index.html", context)


def add_to_group(request, group_id):
	group = Group.objects.get(id= group_id)
	group.participants.add(request.user)
	group.save()
	return redirect("index")


def view_group(request, group_id):
	remove_nav = True
	group = Group.objects.get(id= group_id)
	
	# check for valid group participants
	if not request.user in group.participants.all():
		return redirect("index")
	
	context = {
		"group": group,
		"remove_nav": remove_nav
	}
	
	return render(request, "chat.html", context)
	

def create_group(request):
	remove_nav = True
	categories = Category.objects.all()
	
	if request.method == "POST":
		name = request.POST.get("name")
		category = request.POST.get("category")
		description = request.POST.get("description")
		
		# get or create category
		category, _ = Category.objects.get_or_create(
			name__iexact=category,
			name=category
		)
		
		Group.objects.create(
			name=name,
			description=description,
			creator=request.user,
			category=category
		)
	
	context = {
		"remove_nav": remove_nav,
		"categories": categories
	}
	
	return render(request, "create-group.html", context)
	

#@redirect_auth_user
#def signup(request):
#	if request.method == "POST":
#		username = request.POST.get("username")
#		email = request.POST.get("email")
#		password1 = request.POST.get("password1")
#		password2 = request.POST.get("password2")
#		
#		if password1 == password2:
#			if User.objects.filter(username=username).exists():
#				messages.error(request, "User with given username already exists")
#			elif User.objects.filter(email=email).exists():
#				messages.error(request, "User with given email already exists")
#			else:
#				User.objects.create_user(
#					username=username,
#					email=email,
#					password=password1)
#				messages.info(request, f"Account for {username} created successfully!!")
#				return redirect("signin")
#		else:
#			messages.error(request, "Passwords do not match")
#		
#	return render(request, "signup.html")

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("signin")
    else:
        form = CustomUserCreationForm()
    return render(request,"signup.html",{"form":form})

@redirect_auth_user
def signin(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password1 = request.POST.get("password1")
		
		user = auth.authenticate(username=username, password=password1)
		
		if user is not None:
			auth.login(request, user)
			messages.info(request, request.user)
			return redirect("index")
		else:
			messages.error(request, "Incorrect username or password")
			return redirect("signin")
		
	return render(request, "signin.html")


@login_required(login_url="signin")
def logout(request):
	auth.logout(request)
	return redirect("signin")


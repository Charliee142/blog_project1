from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *


def index(request):
	recent_post = Post.objects.filter(section='Recent').order_by('-id')[0:4]
	main_post = Post.objects.filter(main_post=True)[0:1]
	categories = Category.objects.all()
	tags = Tag.objects.all()
	posts = Post.objects.all().filter(is_published=True).order_by('-created_on')

	
    # Add Paginator
	paginator = Paginator(posts, 4) 
	page = request.GET.get('page')
	
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	

	context = {
        'main_post':main_post,
        'recent_post':recent_post,
        'categories':categories,
        'posts': posts,
        'tags': tags,
    }
	return render(request, "blog_home.html", context)	



def post(request, slug):
	requested_post = Post.objects.get(slug=slug)
	categories = Category.objects.all()
	tags = Tag.objects.all()

	# Related Posts
 	## Get all the tags related to this article
	post_tags = requested_post.tags.all()
	## Filter all posts that contain tags which are related to the current post, and exclude the current post
	related_posts_ids = (Post.objects.all().filter(tags__in=post_tags).exclude(id=requested_post.id) .values_list("id"))
	related_posts = Post.objects.filter(pk__in=related_posts_ids)


	context={
        'categories':categories,
        'tags': tags,
		'post': requested_post,
		'related_posts': related_posts,
	}

	return render(request, "blog_single.html", context)


def category(request, slug):
	posts = Post.objects.filter(categories__slug=slug).filter(is_published=True)
	requested_category = Category.objects.get(slug=slug)
	categories = Category.objects.all()
	recent_post = Post.objects.filter(section='Recent').order_by('-id')[0:4]
	main_post = Post.objects.filter(main_post=True)[0:1]
	tags = Tag.objects.all()

	 # Add Paginator
	paginator = Paginator(posts, 1) 
	page = request.GET.get('page')
	
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	

	context = {
		'tags': tags,
		'posts': posts,
		'main_post':main_post,
		'recent_post':recent_post,
		'category': requested_category,
		'categories': categories,
		
	}
	return render(request, "category.html", context)


def tag(request, slug):
	posts = Post.objects.filter(tags__slug=slug).filter(is_published=True)
	categories = Category.objects.all()
	tags = Tag.objects.all()
	requested_tag = Tag.objects.get(slug=slug)

	 # Add Paginator
	paginator = Paginator(posts, 1) 
	page = request.GET.get('page')
	
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {
		'tags': tags,
		'category': requested_tag,
		'categories': categories,
		'posts': posts,
	}
	return render(request, "tag.html", context) 

def search(request):
	categories = Category.objects.all()
	tags = Tag.objects.all()

	""" search function  """
	query = request.POST.get("search")
	if query:
		posts = Post.objects.filter(is_published=True).filter(title__icontains=query)
	else:
		posts = []

	context = {
		'categories':categories,
		'tags':tags,
		'posts':posts,
		'query': query,
	}
	return render(request, "search.html", context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact = Contact(
            name = name,
            email = email,
            message = message,    
        )
        contact.save()
        return redirect('index')
    return render(request, "contact.html")


def about(request):
   return render(request, "about.html")


def my_account(request):
    my_account = request.user.profile
    context = {
		"account": my_account
	}
    return render(request, "account/my_account.html", context)


def profile(request, pk):
    user_profile = Profile.objects.get(profile_id=pk)
    context = {
		"profile": user_profile
	}
    return render(request, "account/user_profile.html", context)


def UpdateProfile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your profile has been updated successfully')
            return redirect('account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context={
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'account/update_profile.html', context)


def DeleteProfile(request):
    profile = request.user.profile
    form = UserUpdateForm(instance=profile)
    if request.method == "POST":
        profile.delete()
        user = request.user
        user.delete()
        #userprofile = UserProfile.objects.get(user=profile)
        #userprofile.delete()
        #messages.info(request, 'Your profile has been deleted successfully!')
        return redirect("index")
    context={
        "form": form
    }
    return render(request, 'account/delete_account.html', context)


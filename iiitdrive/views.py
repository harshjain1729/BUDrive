
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.conf.urls.static import static
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import models

from .forms import NewUserCreationForm
from .utils import send_email, get_storage_used
from .models import UserDetails, Social, ResourceFile, UserFiles, Post, Tag, Like, Comment

User = get_user_model()

def indexpage(request):
    #print("hello world")
    return render(request, 'index.html')


def signup(request):
	if request.method == 'POST':
		form = NewUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()

			current_site = request.get_host()
			subject = 'Email Verification'

			message = render_to_string(
				'verification_email.html', {
				'username': user.username,
				'domain': current_site,
				'token': user.email_verification_token,
			})
			send_email(subject, user.email, message)

			request.method = 'GET'
			context = {'alert_message' : 'Account Created Successfully, Check Email Inbox for Verification Link'}
			return login(request, **context)
	else:
		form = NewUserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})


def verify_email(request, token) :
	user = User.objects.filter(email_verification_token = token).first()

	if user is None :
		return redirect('home') #bad token, show error or so
	elif user.email_verified :
		return redirect('home') #email already verified
	else :
		user.email_verified = True
		user.is_active = True
		user.save()
		auth_login(request, user)
		return redirect('home')

def login(request, *args, **kwargs):
	context = kwargs

	form = AuthenticationForm()
	context.update({'form' : form})
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user:
			if user.is_active:
				auth_login(request, user)
				return redirect('home')
		else:
			messages.error(request, 'Incorrect Username or Password. Please enter a correct Username and Password.')

	return render(request, 'registration/login.html', context)


@login_required
def homepage(request):
	user = request.user
	if request.method == 'POST':
		if 'message' in request.POST:
			text = request.POST['message']
			tags = request.POST.getlist('hashtag', [])
			file = request.FILES.get('img_file', None)

			post = Post()
			post.owner = request.user
			post.text = text
			if file is not None :
				r = ResourceFile.objects.create(file=file)
				post.file = r
			post.save()

			for tag in tags:
				t, is_created = Tag.objects.get_or_create(name = tag)
				post.tags.add(t)
			post.save()

			return redirect(homepage)
		elif 'comment' in request.POST and 'comment_post' in request.POST :
			post = Post.objects.filter(uid = request.POST['comment_post']).first()
			if post is not None :
				comment = Comment()
				comment.user=user
				comment.post=post
				comment.comment=request.POST['comment']
				comment.save()

			return redirect(homepage)
		elif 'liked_post' in request.POST :
			post = Post.objects.filter(uid = request.POST['liked_post']).first()
			if post is not None :
				like = Like.objects.get_or_create(user=user, post=post)
			return redirect(homepage)

	posts = Post.objects.all().order_by('-created_at')
	context = {'posts': posts}

	return render(request, 'home.html', context)

@login_required
def profile(request):
	user_details = UserDetails.objects.get(user = request.user)
	if request.method == 'POST':
		if 'profile_image' in request.FILES :
			user_details.profile_picture = request.FILES['profile_image']
			user_details.save()
			return redirect(profile)
		else:
			if 'about_me' in request.POST :
				user_details.about_me = request.POST['about_me']
				user_details.save()
			for social in ['github', 'linkedin', 'twitter', 'instagram', 'facebook', 'reddit'] :
				if social in request.POST :
					if Social.objects.filter(user_details = user_details, name = social).exists() :
						user_social = Social.objects.get(user_details = user_details, name = social)
					else :
						user_social = Social()
						user_social.user_details = user_details
						user_social.name = social
					user_social.link = request.POST[social]
					user_social.save()
			return redirect(profile)

	return render(request, 'profile.html')


@login_required
def mydrive(request):
	user = request.user
	files = UserFiles.objects.filter(models.Q(owner=user) & models.Q(is_trashed=False) & models.Q(is_deleted=False))

	if request.method == 'POST':
		if 'document' in request.FILES :
			for f in request.FILES.getlist('document'):
				r_file = ResourceFile.objects.create(file = f)
				UserFiles.objects.create(owner=user, file=r_file)
			return redirect(mydrive)
		elif 'rename_id' in request.POST and 'rename' in request.POST :
			file = files.filter(file__uid = request.POST['rename_id']).first()
			if file is not None :
				file.file.name = request.POST['rename']
				file.file.save()
			return redirect(mydrive)
		elif 'star_id' in request.POST :
			file = files.filter(file__uid = request.POST['star_id']).first()
			if file is not None :
				file.is_starred = not(file.is_starred)
				file.save()
			return redirect(mydrive)
		elif 'trash_id' in request.POST :
			file = files.filter(file__uid = request.POST['trash_id']).first()
			if file is not None :
				file.is_trashed = True
				file.save()
			return redirect(mydrive)
		elif 'share' in request.POST and 'share_id' in request.POST :
			share_username = request.POST['share']
			if share_username != user.username :
				shared_user = get_user_model().objects.filter(username = share_username).first()
				file = files.filter(file__uid = request.POST['share_id']).first()
				if shared_user is not None and file is not None :
					file.shared_with.add(shared_user)
					file.save()
			return redirect(mydrive)

	storage_used = get_storage_used(user.username)

	context = {'files' : files, 'storage_used' : storage_used}
	return render(request, 'mydrive.html', context)

@login_required
def starred(request):
	user = request.user
	files = UserFiles.objects.filter(models.Q(owner=user) & models.Q(is_starred=True) & models.Q(is_trashed=False) & models.Q(is_deleted=False))

	if request.method == 'POST' :
		if 'unstar_id' in request.POST :
			file = files.filter(file__uid = request.POST['unstar_id']).first()
			if file is not None :
				file.is_starred = False
				file.save()
			return redirect(mydrive)
		elif 'trash_id' in request.POST :
			file = files.filter(file__uid = request.POST['trash_id']).first()
			if file is not None :
				file.is_trashed = True
				file.save()
			return redirect(mydrive)

	context = {'files' : files}
	return render(request, 'starred.html', context)


@login_required
def trash(request):
	user = request.user
	files = UserFiles.objects.filter(models.Q(owner=user) & models.Q(is_trashed=True) & models.Q(is_deleted=False))
	print(request.POST)
	if request.method == 'POST' :
		if 'delete_id' in request.POST :
			file = files.filter(file__uid = request.POST['delete_id']).first()
			if file is not None :
				file.is_deleted = True
				file.save()
			return redirect(mydrive)
		elif 'restore_id' in request.POST :
			file = files.filter(file__uid = request.POST['restore_id']).first()
			if file is not None :
				file.is_trashed = False
				file.save()
			return redirect(mydrive)

	context = {'files' : files}
	return render(request, 'trash.html', context)

@login_required
def social(request):
    return render(request, 'social.html')


@login_required
def share(request):
	user = request.user
	files = user.shared_files.filter(models.Q(is_trashed=False) & models.Q(is_deleted=False))

	context = {'files' : files}
	return render(request, 'share.html', context)

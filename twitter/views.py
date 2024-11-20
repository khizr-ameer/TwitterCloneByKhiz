
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Profile,tweet
from .forms import TweetForm,SignUpForm,ProfilePicForm
from django.contrib.auth.models import User

# Create your views here.

#function for viewing the homepage
def userhome(request):
    if request.user.is_authenticated:
        form=TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                Tweet = form.save(commit=False)
                Tweet.user = request.user
                Tweet.save()
                messages.success(request, ("Your Tweet is Posted !"))
                return redirect('home')
            
        tweets = tweet.objects.all().order_by("-created_at")
        return render(request, 'userhome.html', {"tweets":tweets, "form":form})
    else:
        tweets = tweet.objects.all().order_by("-created_at")
        return render(request, 'userhome.html', {"tweets":tweets})
    


#function for list of profiles
def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		profile = Profile.objects.get(user_id=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles, "profile":profile})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')


#function for Profile
def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id=pk)
		tweets = tweet.objects.filter(user_id=pk).order_by("-created_at")

		# Post Form logic
		if request.method == "POST":
			# Get current user
			current_user_profile = request.user.profile
			# Get form data
			action = request.POST['follow']
			# Decide to follow or unfollow
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			# Save the profile
			current_user_profile.save()

		return render(request, "userprofile.html", {"profile":profile, "tweets":tweets})
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')	
        


#function for login
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You are logged in Twitter :) "))
			return redirect('home')
		else:
			messages.success(request, ("Retry your Username and Password. Please Try Again :( "))
			return redirect('login')

	else:
		return render(request, "login.html", {})

#function for logout
def logout_user(request):
    logout(request)
    messages.success(request, ("You Logged Out Successfully!"))
    return redirect('home')

#function for new User Registraton
def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome to Twitter :) "))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})


#funcion to see Followers   
def followers(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			profile = Profile.objects.get(user_id=pk)
			return render(request, 'followers.html', {"profiles":profiles,'profile':profile})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')  

#function to see following
def follows(request, pk):
	if request.user.is_authenticated:
		if request.user.id == pk:
			profiles = Profile.objects.get(user_id=pk)
			profile = Profile.objects.get(user_id=pk)
			return render(request, 'follows.html', {"profiles":profiles,"profile":profile})
		else:
			messages.success(request, ("That's Not Your Profile Page..."))
			return redirect('home')	
	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')   

#function for deleting the tweet
def delete_tweet(request, pk):
	if request.user.is_authenticated:
		tweets1 = get_object_or_404(tweet, id=pk)
		# Check to see if you own the tweet
		if request.user.username == tweets1.user.username:
			# Delete The tweer
			tweets1.delete()
			
			messages.success(request, ("The twwet Has Been Deleted!"))
			return redirect(request.META.get("HTTP_REFERER"))	
		else:
			messages.success(request, ("You Don't Own That Tweet!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect(request.META.get("HTTP_REFERER"))



#function for Editing the Tweet
def edit_tweet(request,pk):
	if request.user.is_authenticated:
		# Grab The Tweet
		tweets1 = get_object_or_404(tweet, id=pk)

		# Check to see if you own the tweet
		if request.user.username == tweets1.user.username:
			
			form = TweetForm(request.POST or None, instance=tweets1)
			if request.method == "POST":
				if form.is_valid():
					tweets1 = form.save(commit=False)
					tweets1.user = request.user
					tweets1.save()
					messages.success(request, ("Your tweet Has Been Updated!"))
					return redirect('home')
			else:
				return render(request, "edit_tweet.html", {'form':form, 'tweets1':tweets1})
	
		else:
			messages.success(request, ("Unable to Update!!"))
			return redirect('home')

	else:
		messages.success(request, ("Please Log In To Continue..."))
		return redirect('home')

def update_user(request):
	if request.user.is_authenticated:
		# current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		# user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if profile_form.is_valid():
			# user_form.save()
			profile_form.save()

			# login(request, current_user)
			messages.success(request, ("Your Profile Pic Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')

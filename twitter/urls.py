
from django.urls import path
from twitter import views
urlpatterns = [

    #these are all the paths for:

    path('',views.userhome, name='home'),
    #to view the list of profiles created
    path('profile_list/',views.profile_list, name='profile_list'),
    #to view the profile
    path('profile/<int:pk>',views.profile, name='profile'),
    #to view the profile followers
    path('profile/followers/<int:pk>',views.followers, name='followers'),
    #to view the following
    path('profile/follows/<int:pk>',views.follows, name='follows'),
    #for the login page page path
    path('login',views.login_user, name='login'),
    #for the logout page path
    path('logout',views.logout_user, name='logout'),
    #for new user to register
    path('register',views.register_user, name='register'),
    #for deleting Tweet path
    path('delete_tweet/<int:pk>',views.delete_tweet, name='delete_tweet'),
    #for editing tweet path
    path('edit_tweet/<int:pk>',views.edit_tweet, name='edit_tweet'),
    #for update user mean profile update path
    path('update_user/', views.update_user, name='update_user')
]

from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, tweet
admin.site.unregister(Group)

#combining the User and Profile Class using stackedinline property
class ProfileInline(admin.StackedInline):
    model=Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model=User
    fields = ["username"]
    inlines = [ProfileInline]

# unregsiter intial user
admin.site.unregister(User)

#reregister user
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)
admin.site.register(tweet)
#mix profike info into user info


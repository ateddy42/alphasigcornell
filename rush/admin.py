from django.contrib import admin
from .models import Rushee, Signin, Comment, Event, Setting, UserComment

class SigninInline(admin.StackedInline):
	model = Signin
	extra = 0

class CommentInline(admin.StackedInline):
	model = Comment
	extra = 0

class EventInline(admin.StackedInline):
	model = Event
	extra = 0

class RusheeAdmin(admin.ModelAdmin):
	fieldsets = [
		('Name', {'fields':
			['first','last']}),
		('Basic Information', {'fields':
			['netid','phone','build','room','active']})
		]
	inlines = [SigninInline, CommentInline, EventInline]

admin.site.register(Rushee, RusheeAdmin)
admin.site.register(Setting)

class UserCommentAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'comments')

admin.site.register(UserComment, UserCommentAdmin)
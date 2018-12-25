from django.contrib import admin
from .models import Rushee, Signin, Comment, Event, Setting, UserComment

# inline edit for Signin model
class SigninInline(admin.StackedInline):
    model = Signin
    extra = 0

# inline edit for Comment model
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

# inline edit for Event model
class EventInline(admin.StackedInline):
    model = Event
    extra = 0

# register Rushee model
class RusheeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields':
            ['first','last']}),
        ('Basic Information', {'fields':
            ['netid','phone','build','room','active']})
        ]
    inlines = [SigninInline, CommentInline, EventInline]

admin.site.register(Rushee, RusheeAdmin)

# register UserComment model
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'comments')
    readonly_fields = ['user']
    fieldsets = [
        (None, {'fields': ['user', 'comments']})
    ]

    def disableCommenting(modeladmin, request, queryset):
        rows_updated = queryset.update(comments=False)
        modeladmin.message_user(request, "Successfully disabled commenting for %s user(s)" % rows_updated)
    disableCommenting.short_description = "Disable Commenting"


    def enableComments(modeladmin, request, queryset):
        rows_updated = queryset.update(comments=True)
        modeladmin.message_user(request, "Successfully enabled commenting for %s user(s)" % rows_updated)
    enableComments.short_description = "Enable Commenting"

    actions = [enableComments, disableCommenting]

admin.site.register(UserComment, UserCommentAdmin)

# register Setting model
class SettingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'settingValue')

    def settingValue(self, obj):
        if obj.char:
            return obj.char
        if obj.val == 0:
            return "&#10060;"
        if obj.val == 1:
            return "&#9989;"
        return obj.val
    settingValue.allow_tags = True
    settingValue.short_description = 'Setting Value'

admin.site.register(Setting, SettingAdmin)
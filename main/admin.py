from django.contrib import admin
from .models import Officer, Brother
from django.forms import TextInput, Textarea
from django.db import models

# register Brother model
class BrotherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'home', 'major', 'year', 'active')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':30})},
    }

    # action to mass-deactivate brothers
    def deactivate(modeladmin, request, queryset):
        rows_updated = queryset.update(active=False)
        modeladmin.message_user(request, "Successfully marked %s brother(s) as inactive" % rows_updated)
    deactivate.short_description = "Mark Inactive"

    # action to mass-activate brothers
    def activate(modeladmin, request, queryset):
        rows_updated = queryset.update(active=True)
        modeladmin.message_user(request, "Successfully marked %s brother(s) as active" % rows_updated)
    activate.short_description = "Mark Active"

    # add actions to page
    actions = [deactivate, activate]

admin.site.register(Brother, BrotherAdmin)

# register Officer model
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('position', 'name', 'email', 'displayed')

    def showOfficer(modeladmin, request, queryset):
        rows_updated = queryset.update(displayed=True)
        modeladmin.message_user(request, "Successfully displayed %s officer(s)" % rows_updated)
    showOfficer.short_description = "Show Officers"

    def hideOfficer(modeladmin, request, queryset):
        rows_updated = queryset.update(displayed=False)
        modeladmin.message_user(request, "Successfully hid %s officer(s)" % rows_updated)
    hideOfficer.short_description = "Hide Officers"

    actions = [showOfficer, hideOfficer]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':30})},
    }

admin.site.register(Officer, OfficerAdmin)
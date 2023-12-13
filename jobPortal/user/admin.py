from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        if hasattr(obj, 'user'):
            obj.user.delete() if obj.user else None

        obj.delete()

# Registering Profile model
admin.site.register(Profile, ProfileAdmin)

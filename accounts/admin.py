from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User
from .models import Relation, Profile, DirectMessage


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('staff_id', 'email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('staff_id', 'email', 'phone_number', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields': ('staff_id','email', 'phone_number', 'username', 'is_admin', 'password1', 'password2')}),
    )
    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()


class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False





admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Relation)
admin.site.register(DirectMessage)
admin.site.register(Profile)

from django.contrib import admin
# from db_connect.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


# Extending the original UserAdmin class that Django admin provides.
# Replacing the use of username for email.
# Registering your new class to be used by Django admin for your new User model.
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    #Define admin model for custom User model with no email field.

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False

# class AccountsUserAdmin(AuthUserAdmin):
#     def add_view(self, *args, **kwargs):
#         self.inlines = []
#         return super(AccountsUserAdmin, self).add_view(*args, **kwargs)
    
#     def change_view(self, *args, **kwargs):
#         self.inlines = [UserProfileInline]
#         return super(AccountsUserAdmin, self).change_view(*args, **kwargs)
#     # inlines = [UserProfileInline]

# admin.site.unregister(User)
# admin.site.register(User, AccountsUserAdmin)
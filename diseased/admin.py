from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import DiseasedUser, StatusDiseasedUser, SpecialDoctor

User = get_user_model()


@admin.register(DiseasedUser)
class DiseasedUserAdmin(admin.ModelAdmin):
    readonly_fields = ['full_name', 'total_cost_of_the_treatments', 'is_doctor_view']


@admin.register(StatusDiseasedUser)
class StatusDiseasedUserAdmin(admin.ModelAdmin):
    pass


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['tel_number', 'email', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ('tel_number', 'email', 'password', 'first_name', 'last_name')}),
        # ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tel_number', 'email', 'first_name', 'last_name', 'password', 'password2')}
         ),
    )
    search_fields = ['tel_number', 'email']
    ordering = ['tel_number', 'email']
    filter_horizontal = ()


@admin.register(SpecialDoctor)
class SpecialDoctorAdmin(admin.ModelAdmin):
    pass

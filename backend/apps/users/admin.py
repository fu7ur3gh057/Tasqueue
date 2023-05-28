from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['pkid', 'id', 'phone_number', 'email', 'role', 'is_verified', 'is_active',
                    'created_at']
    list_display_links = ['id', 'email']
    list_filter = ['email', 'role', 'is_verified', 'is_active']
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "phone_number",
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "is_verified",
                    # "groups",
                    # "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role"),
            },
        ),
    )
    search_fields = ["email", "is_verified"]


admin.site.register(User, UserAdmin)

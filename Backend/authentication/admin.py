from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role

admin.site.register(Role)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (None, 
        {
            "fields": (
                "bio",
                "profile_pic",
            )
        },
        ),
        (
            "Roles",
            {
                "fields": (
                    'roles',
                )
            },
        )
    )
    filter_horizontal = (
        *UserAdmin.filter_horizontal, "roles"
    )
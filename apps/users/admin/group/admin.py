from django.contrib import admin
from django.contrib.auth.models import Group

from .custom_role_form import CustomRoleForm

admin.site.unregister(Group)


@admin.register(Group)
class CustomRoleAdmin(admin.ModelAdmin):
    form = CustomRoleForm
    filter_horizontal = ("permissions",)

    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "id",
        "name",
    )
    ordering = (
        "-id",
        "name",
    )
    list_display_links = (
        "id",
        "name",
    )

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False

from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.utils.safestring import mark_safe


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def grupos(self, obj):
        nombres = [v.name for v in Group.objects.filter(permissions=obj)]
        return mark_safe("<br>\n".join(nombres))

    list_display = ("id", "name", "grupos")
    search_fields = (
        "id",
        "name",
    )
    list_filter = ("group__name",)
    ordering = (
        "-id",
        "name",
    )
    list_display_links = (
        "id",
        "name",
    )
    fieldsets = ((None, {"fields": ("name",)}),)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

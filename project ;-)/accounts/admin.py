from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'role', 'company_name', 'phone', 'is_approved', 'created_at']
    list_filter   = ['role', 'is_approved']
    search_fields = ['user__username', 'company_name']
    actions       = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        queryset.filter(role='supplier').update(is_approved=True)
        self.message_user(request, "Selected suppliers approved.")
    approve_selected.short_description = "Approve selected suppliers"

    def reject_selected(self, request, queryset):
        queryset.filter(role='supplier').update(is_approved=False)
        self.message_user(request, "Selected suppliers rejected.")
    reject_selected.short_description = "Reject selected suppliers"

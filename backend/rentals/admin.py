from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SkiBuddy, Rental, Appointment, Photo, Vehicle, WaiverAgreement
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_ski_buddy')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'is_ski_buddy')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'is_ski_buddy')}),
    )

class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'start_time', 'end_time', 'jet_ski_image_preview')

    def jet_ski_image_preview(self, obj):
        if obj.vehicle and obj.vehicle.image:
            return format_html('<img src="{}" width="100" style="object-fit: cover;" />', obj.vehicle.image.url)
        return "No image"

    jet_ski_image_preview.short_description = 'Vehicle Image'

admin.site.register(Rental, RentalAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(SkiBuddy)
admin.site.register(Appointment)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption']

@admin.register(Vehicle)
class JetSkiAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available']

@admin.register(WaiverAgreement)
class WaiverAgreementAdmin(admin.ModelAdmin):
    list_display = ('user', 'version', 'accepted_at')
    search_fields = ('user__username', 'version')
    list_filter = ('version', 'accepted_at')
from django.contrib import admin
from django.contrib import messages
from .models import IncludeBootstrap


@admin.register(IncludeBootstrap)
class IncludeBootstrapAdmin(admin.ModelAdmin):
    fields = ('library', 'version', 'url_pattern', 'integrity', 'url', 'active')
    readonly_fields = ('integrity', 'url')
    list_display = ('library', 'version', 'active')

    def save_model(self, request, obj, form, change):
        if obj.active and obj.__class__.objects.filter(library=obj.library, active=obj.active).exists():
            obj.__class__.objects.filter(library=obj.library, active=obj.active).update(active=False)
            messages.add_message(request, messages.WARNING,
                                 f'Please note! The object was activated and another library was deactivated.')
        super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import IncludeBootstrap


@admin.register(IncludeBootstrap)
class IncludeBootstrapAdmin(admin.ModelAdmin):
    fields = ('library', 'version', 'url_pattern', 'integrity', 'url')
    readonly_fields = ('integrity', 'url')
    list_display = ('library', 'version')

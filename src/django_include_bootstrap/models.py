from django.db import models


class IncludeBootstrap(models.Model):
    LIBRARY = ((1, 'Bootstrap'), (2, 'Jquery'), (3, 'Popover'))

    library = models.CharField(max_length=32, choices=LIBRARY)
    version = models.CharField(max_length=8)
    integrity = models.CharField(max_length=255)
    url = models.URLField(verbose_name='Library cdn url')
    url_pattern = models.CharField(max_length=512,
                                   help_text='Should be string like - https://code.jquery.com/jquery-{version}.js, '
                                             '{version} is a variable that will be replaced with values '
                                             'from "version" field')

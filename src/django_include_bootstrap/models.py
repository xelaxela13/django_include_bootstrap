from django.db import models
from django.core.exceptions import ValidationError
from requests import get
import subresource_integrity as integrity


class IncludeBootstrap(models.Model):
    LIBRARY = (('1', 'Bootstrap Js'), ('2', 'Jquery'), ('3', 'Popover Js'), ('4', 'Bootstrap Css'))

    library = models.CharField(max_length=32, choices=LIBRARY, blank=False, null=False)
    version = models.CharField(max_length=8, blank=False, null=False)
    integrity = models.CharField(max_length=255)
    url = models.URLField(verbose_name='Library cdn url')
    url_pattern = models.CharField(max_length=512,
                                   help_text='Should be string like - https://code.jquery.com/jquery-{version}.js, '
                                             '{version} is a variable that will be replaced with values '
                                             'from "version" field',
                                   blank=False, null=False)
    active = models.BooleanField(default=True)

    @classmethod
    def get_active_instance(cls, library):
        return cls.objects.filter(active=True, library=library).first()

    def clean(self):
        super().clean()
        if self.url_pattern.count('{') != 1 or self.url_pattern.count('}') != 1 or \
                self.url_pattern.count('{version}') != 1:
            raise ValidationError('Wrong url pattern string!')
        url = self.url_pattern.format(version=self.version)
        response = get(url)
        if response and response.status_code == 200:
            self.url = url
            self.integrity = integrity.render(response.content)
        else:
            raise ValidationError(f'Wrong library version or url_pattern, {url} does not exists!')

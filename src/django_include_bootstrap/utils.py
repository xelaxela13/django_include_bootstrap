from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.utils.html import format_html
from itertools import chain
import requests
import subresource_integrity as integrity

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

CDNS = {
    "bootstrap_cdn_url": "https://stackpath.bootstrapcdn.com/bootstrap/{bootstrap_version}",
    "jquery_cdn_url": "https://code.jquery.com",
    "popover_cdn_url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/{popover_version}/umd",
}
VERSIONS = {
    "bootstrap_version": "4.1.1",
    "jquery_version": "3.3.1",
    "popover_version": "1.14.3",
}
DEFAULTS = {
    "css_url": {
        "href": "{bootstrap_cdn_url}/css/bootstrap.{min}css",
        "integrity": "sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "{bootstrap_cdn_url}/js/bootstrap.{min}js",
        "integrity": "sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T",
        "crossorigin": "anonymous",
    },
    "jquery_url": {
        "url": "{jquery_cdn_url}/jquery-{jquery_version}.{min}js",
        "integrity": "sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI/8aZajjp4Bqd+V6D5IgvKT",
        "crossorigin": "anonymous",
    },
    "jquery_slim_url": {
        "url": "{jquery_cdn_url}/jquery-{jquery_version}.slim.{min}js",
        "integrity": "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
        "crossorigin": "anonymous",
    },
    "popper_url": {
        "url": "{popover_cdn_url}/popper.min.js",
        "integrity": "sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
        "crossorigin": "anonymous",
    },
}
INCLUDE_BOOTSTRAP_SETTINGS = {
    **VERSIONS,
    "javascript_in_head": False,
    "include_jquery": False,
    "use_i18n": False,
    "min": True
}


def fetch(url):
    response = requests.get(url=url)
    yield response


def main(url):
    pass


def format_bootstrap_settings(ib_setting, ib_modify_dict):
    for key in chain(CDNS, VERSIONS):
        try:
            ib_setting[key]
        except KeyError:
            ib_setting[key] = INCLUDE_BOOTSTRAP_SETTINGS[key]
    format_keys = {'bootstrap_cdn_url': ib_setting['bootstrap_cdn_url'],
                   'jquery_cdn_url': ib_setting['jquery_cdn_url'],
                   'popover_cdn_url': ib_setting['popover_cdn_url'],
                   'min': 'min.' if ib_setting['min'] else '',
                   "bootstrap_version": ib_setting['bootstrap_version'],
                   "jquery_version": ib_setting['jquery_version'],
                   "popover_version": ib_setting['popover_version'],
                   }
    for key, val in ib_modify_dict.items():
        if isinstance(val, dict) and val.get('href'):
            val['href'] = val['href'].format(**format_keys)
        else:
            ib_modify_dict[key] = val.format(**format_keys)
    return ib_modify_dict


def get_bootstrap_setting(name, default=None):
    """Read a setting."""
    # Start with a copy of default settings
    IB_SETTINGS = INCLUDE_BOOTSTRAP_SETTINGS.copy()
    IB_CDNS = CDNS.copy()
    IB_SETTINGS.update(**IB_CDNS)

    IB_DEFAULTS = format_bootstrap_settings(IB_SETTINGS, DEFAULTS.copy())
    IB_SETTINGS.update(**IB_DEFAULTS)
    # Override with user settings from settings.py
    IB_SETTINGS.update(getattr(settings, "INCLUDE_BOOTSTRAP_SETTINGS", {}))
    # Update use_i18n
    IB_SETTINGS["use_i18n"] = i18n_enabled()

    return IB_SETTINGS.get(name, default)


def jquery_url():
    """Return the full url to jQuery library file to use."""
    return get_bootstrap_setting("jquery_url")


def jquery_slim_url():
    """Return the full url to slim jQuery library file to use."""
    return get_bootstrap_setting("jquery_slim_url")


def include_jquery():
    """
    Return whether to include jquery.

    Setting could be False, True|'full', or 'slim'
    """
    return get_bootstrap_setting("include_jquery")


def popper_url():
    """Return the full url to Popper file."""
    return get_bootstrap_setting("popper_url")


def javascript_url():
    """Return the full url to the Bootstrap JavaScript file."""
    return get_bootstrap_setting("javascript_url")


def javascript_bundle_url():
    """Return the full url to the Bootstrap JavaScript file."""
    return get_bootstrap_setting("javascript_bundle_url")


def css_url():
    """Return the full url to the Bootstrap CSS file."""
    return get_bootstrap_setting("css_url")


def i18n_enabled():
    """Return the projects i18n setting."""
    return getattr(settings, "USE_I18N", False)


def sanitize_url_dict(url, url_attr="src"):
    """Sanitize url dict as used in django-bootstrap4 settings."""
    if isinstance(url, str):
        return {url_attr: url}
    return url.copy()


def text_value(value):
    """Force a value to text, render None as an empty string."""
    if value is None:
        return ""
    return force_text(value)


def render_script_tag(url):
    """Build a script tag."""
    url_dict = sanitize_url_dict(url)
    url_dict.setdefault("src", url_dict.pop("url", None))
    return render_tag("script", url_dict)


def render_link_tag(url, rel="stylesheet", media=None):
    """Build a link tag."""
    url_dict = sanitize_url_dict(url, url_attr="href")
    url_dict.setdefault("href", url_dict.pop("url", None))
    url_dict["rel"] = rel
    if media:
        url_dict["media"] = media
    return render_tag("link", attrs=url_dict, close=False)


def render_tag(tag, attrs=None, content=None, close=True):
    """Render a HTML tag."""
    builder = "<{tag}{attrs}>{content}"
    if content or close:
        builder += "</{tag}>"
    return format_html(builder, tag=tag, attrs=mark_safe(flatatt(attrs)) if attrs else "", content=text_value(content))


if __name__ == "__main__":
    main()

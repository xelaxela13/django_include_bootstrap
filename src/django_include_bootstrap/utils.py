from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.utils.html import format_html
import requests
import subresource_integrity as integrity
from copy import deepcopy

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

VERSIONS = {
    "bootstrap_version": "4.4.1",
    "jquery_version": "3.3.1",
    "popover_version": "1.14.3",
}

INCLUDE_BOOTSTRAP_SETTINGS = {
    **VERSIONS,
    "javascript_in_head": False,
    "include_jquery": False,
    "use_i18n": False,
    "min": True,
}


def main():
    jquery_url()


def get_integrity(data):
    return integrity.render(data)


def generate_urls_settings(setting: dict) -> dict:
    minify = 'min.' if setting.get('min', INCLUDE_BOOTSTRAP_SETTINGS['min']) else ''
    bootstrap_version = setting.get('bootstrap_version', VERSIONS['bootstrap_version'])
    jquery_version = setting.get('jquery_version', VERSIONS['jquery_version'])
    popover_version = setting.get('popover_version', VERSIONS['popover_version'])
    urls_settings = {
        "css_url": {
            "href": f"https://stackpath.bootstrapcdn.com/bootstrap/{bootstrap_version}/css/bootstrap.{minify}css",
            "integrity": "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
            "crossorigin": "anonymous",
        },
        "javascript_url": {
            "url": f"https://stackpath.bootstrapcdn.com/bootstrap/{bootstrap_version}/js/bootstrap.{minify}js",
            "integrity": "sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6",
            "crossorigin": "anonymous",
        },
        "jquery_url": {
            "url": f"https://code.jquery.com/jquery-{jquery_version}.{minify}js",
            "integrity": "sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI/8aZajjp4Bqd+V6D5IgvKT",
            "crossorigin": "anonymous",
        },
        "jquery_slim_url": {
            "url": f"https://code.jquery.com//jquery-{jquery_version}.slim.{minify}js",
            "integrity": "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
            "crossorigin": "anonymous",
        },
        "popper_url": {
            "url": f"https://cdnjs.cloudflare.com/ajax/libs/popper.js/{popover_version}/umd/popper.{minify}js",
            "integrity": "sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
            "crossorigin": "anonymous",
        },
    }
    return urls_settings


def get_bootstrap_setting(name, default=None, request_files=True):
    """Read a setting."""
    # Start with a copy of default settings
    SETTINGS = deepcopy(INCLUDE_BOOTSTRAP_SETTINGS)

    # Override with user settings from settings.py
    # SETTINGS.update(getattr(settings, "INCLUDE_BOOTSTRAP_SETTINGS", {}))
    SETTINGS.update({'bootstrap_version': '5.4.3'})
    # FORMATED = format_bootstrap_settings(SETTINGS, request_files)
    # SETTINGS.update(**FORMATED)
    URLS = generate_urls_settings(SETTINGS)
    SETTINGS.update(**URLS)
    # Update use_i18n
    # SETTINGS["use_i18n"] = i18n_enabled()
    print(SETTINGS)
    return SETTINGS.get(name, default)


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

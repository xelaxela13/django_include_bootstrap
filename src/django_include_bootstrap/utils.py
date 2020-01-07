from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.utils.html import format_html

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

# Default settings

INCLUDE_BOOTSTRAP_DEFAULTS = {
    "css_url": {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css",
        "integrity": "sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js",
        "integrity": "sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T",
        "crossorigin": "anonymous",
    },
    "theme_url": None,
    "jquery_url": {
        "url": "https://code.jquery.com/jquery-3.3.1.min.js",
        "integrity": "sha384-tsQFqpEReu7ZLhBV2VZlAu7zcOV+rXbYlF2cqB8txI/8aZajjp4Bqd+V6D5IgvKT",
        "crossorigin": "anonymous",
    },
    "jquery_slim_url": {
        "url": "https://code.jquery.com/jquery-3.3.1.slim.min.js",
        "integrity": "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
        "crossorigin": "anonymous",
    },
    "popper_url": {
        "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
        "integrity": "sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49",
        "crossorigin": "anonymous",
    },
    "javascript_in_head": False,
    "include_jquery": False,
    "use_i18n": False,
}


def get_bootstrap_setting(name, default=None):
    """Read a setting."""
    # Start with a copy of default settings
    INCLUDE_BOOTSTRAP = INCLUDE_BOOTSTRAP_DEFAULTS.copy()

    # Override with user settings from settings.py
    INCLUDE_BOOTSTRAP.update(getattr(settings, "INCLUDE_BOOTSTRAP", {}))

    # Update use_i18n
    INCLUDE_BOOTSTRAP["use_i18n"] = i18n_enabled()

    return INCLUDE_BOOTSTRAP.get(name, default)


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


def theme_url():
    """Return the full url to the theme CSS file."""
    return get_bootstrap_setting("theme_url")


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

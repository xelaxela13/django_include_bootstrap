from django import template

from django.utils.safestring import mark_safe

from ..utils import (
    css_url,
    get_bootstrap_setting,
    javascript_url,
    javascript_bundle_url,
    jquery_slim_url,
    jquery_url,
    popper_url,
    fontawesome_css_url,
    render_link_tag,
    render_script_tag,
    render_tag,
)

register = template.Library()


@register.filter
def bootstrap_setting(value):
    """
    Get a setting.

    A simple way to read bootstrap settings in a template.
    Please consider this filter private for now, do not use it in your own templates.
    """
    return get_bootstrap_setting(value)


@register.simple_tag
def bootstrap_jquery_url():
    """
    Return url to full version of jQuery.

    **Tag name**::

        bootstrap_jquery_url

    Return the full url to jQuery plugin to use

    Default value: ``https://code.jquery.com/jquery-3.2.1.min.js``

    This value is configurable, see Settings section

    **Usage**::

        {% bootstrap_jquery_url %}

    **Example**::

        {% bootstrap_jquery_url %}
    """
    return jquery_url()


@register.simple_tag
def bootstrap_jquery_slim_url():
    """
    Return url to slim version of jQuery.

    **Tag name**::

        bootstrap_jquery_slim_url

    Return the full url to slim jQuery plugin to use

    Default value: ``https://code.jquery.com/jquery-3.2.1.slim.min.js``

    This value is configurable, see Settings section

    **Usage**::

        {% bootstrap_jquery_slim_url %}

    **Example**::

        {% bootstrap_jquery_slim_url %}
    """
    return jquery_slim_url()


@register.simple_tag
def bootstrap_popper_url():
    """
    Return the full url to the Popper plugin to use.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        bootstrap_popper_url

    **Usage**::

        {% bootstrap_popper_url %}

    **Example**::

        {% bootstrap_popper_url %}
    """
    return popper_url()


@register.simple_tag
def bootstrap_javascript_url():
    """
    Return the full url to the Bootstrap JavaScript library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        bootstrap_javascript_url

    **Usage**::

        {% bootstrap_javascript_url %}

    **Example**::

        {% bootstrap_javascript_url %}
    """
    return javascript_url()


@register.simple_tag
def bootstrap_javascript_bundle_url():
    """
    Return the full url to the Bootstrap JavaScript library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        bootstrap_javascript_bundle_url

    **Usage**::

        {% bootstrap_javascript_bundle_url %}

    **Example**::

        {% bootstrap_javascript_bundle_url %}
    """
    return javascript_bundle_url()


@register.simple_tag
def bootstrap_css_url():
    """
    Return the full url to the Bootstrap CSS library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        bootstrap_css_url

    **Usage**::

        {% bootstrap_css_url %}

    **Example**::

        {% bootstrap_css_url %}
    """
    return css_url()


@register.simple_tag
def bootstrap_css():
    """
    Return HTML for Bootstrap CSS. Adjust url in settings. If no url is returned, we don't want this statement to return any HTML. This is intended behavior.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        bootstrap_css

    **Usage**::

        {% bootstrap_css %}

    **Example**::

        {% bootstrap_css %}
    """
    rendered_urls = []
    if bootstrap_css_url():
        rendered_urls.append(render_link_tag(bootstrap_css_url()))
    return mark_safe("".join([url for url in rendered_urls]))


@register.simple_tag
def fontawesome_url():
    """
    Return the full url to the Fontawesome CSS library.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        fontawesome_url

    **Usage**::

        {% fontawesome_url %}

    **Example**::

        {% fontawesome_url %}
    """
    return fontawesome_css_url()


@register.simple_tag
def fontawesome_css():
    """
        Return HTML for Fontawesome CSS. Adjust url in settings. If no url is returned, we don't want this statement to return any HTML. This is intended behavior.

        Default value: ``None``

        This value is configurable, see Settings section

        **Tag name**::

            fontawesome_css

        **Usage**::

            {% fontawesome_css %}

        **Example**::

            {% fontawesome_css %}
        """
    rendered_urls = []
    if fontawesome_url():
        rendered_urls.append(render_link_tag(fontawesome_url()))
    return mark_safe("".join([url for url in rendered_urls]))


@register.simple_tag
def bootstrap_jquery(jquery=True):
    """
    Return HTML for jQuery tag.

    Adjust the url dict in settings.
    If no url is returned, we don't want this statement to return any HTML. This is intended behavior.

    This value is configurable, see Settings section. Note that any value that evaluates to True and is
    not "slim" will be interpreted as True.

    **Tag name**::

        bootstrap_jquery

    **Parameters**:

        :jquery: False|"slim"|True (default=True)

    **Usage**::

        {% bootstrap_jquery %}

    **Example**::

        {% bootstrap_jquery jquery='slim' %}
    """
    if not jquery:
        return ""
    elif jquery == "slim":
        jquery = get_bootstrap_setting("jquery_slim_url")
    else:
        jquery = get_bootstrap_setting("jquery_url")

    if isinstance(jquery, str):
        jquery = dict(src=jquery)
    else:
        jquery = jquery.copy()
        jquery.setdefault("src", jquery.pop("url", None))

    return render_tag("script", attrs=jquery)


@register.simple_tag
def bootstrap_javascript(jquery=False, popover=False, bundle=False):
    """
    Return HTML for Bootstrap JavaScript.

    Adjust url in settings.
    If no url is returned, we don't want this statement to return any HTML. This is intended behavior.

    Default value: False

    This value is configurable, see Settings section. Note that any value that evaluates to True and is
    not "slim" will be interpreted as True.

    **Tag name**::

        bootstrap_javascript

    **Parameters**:

        :jquery: False|"slim"|True (default=False)
        :popover: False|True (default=False)
        :bundle: False|True (default=False)

    **Usage**::

        {% bootstrap_javascript %}

    **Example**::

        {% bootstrap_javascript jquery="slim" popover="True" bundle="True" %}
    """
    # List of JS tags to include
    javascript_tags = []

    # Get jquery value from setting or leave default.
    jquery = jquery or get_bootstrap_setting("include_jquery", False)

    # Include jQuery if the option is passed
    if jquery:
        javascript_tags.append(bootstrap_jquery(jquery=jquery))

    # Popper.js library
    if popover and not bundle:
        javascript_tags.append(render_script_tag(bootstrap_popper_url()))

    # Bootstrap 4 JavaScript, Bundle already include popover
    bootstrap_js_url = bootstrap_javascript_url() if not bundle else bootstrap_javascript_bundle_url()
    if '.bundle' in bootstrap_js_url['url'] and popover and not bundle:
        javascript_tags.pop()

    if bootstrap_js_url:
        javascript_tags.append(render_script_tag(bootstrap_js_url))

    # Join and return
    return mark_safe("\n".join(javascript_tags))

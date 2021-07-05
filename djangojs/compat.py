try:
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver, get_script_prefix
except ImportError:
    from django.urls import URLPattern as RegexURLPattern, URLResolver as RegexURLResolver, get_script_prefix

from django.conf import settings

# Borrowed from DRF
def get_regex_pattern(urlpattern):
    if hasattr(urlpattern, 'pattern'):
        # Django 2.0
        return urlpattern.pattern.regex.pattern
    else:
        # Django < 2.0
        return urlpattern.regex.pattern


def make_url_resolver(regex, urlpatterns):
    try:
        # Django 2.0
        from django.urls.resolvers import RegexPattern
        return RegexURLResolver(RegexPattern(regex), urlpatterns)

    except ImportError:
        # Django < 2.0
        return RegexURLResolver(regex, urlpatterns)


middleware = getattr(settings, 'MIDDLEWARE_CLASSES', 'MIDDLEWARE')

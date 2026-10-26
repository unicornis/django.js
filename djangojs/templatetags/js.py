# -*- coding: utf-8 -*-
'''
Provide template tags to help with Javascript/Django integration.
'''
from __future__ import unicode_literals

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe

from djangojs import JQUERY_MIGRATE_VERSION
from djangojs.conf import settings

register = template.Library()


@register.simple_tag
def js_lib(filename):
    return javascript('js/libs/%s' % filename)


@register.simple_tag
def javascript(filename, type='text/javascript'):
    '''A simple shortcut to render a ``script`` tag to a static javascript file'''
    if '?' in filename and len(filename.split('?')) == 2:
        filename, params = filename.split('?')
        return mark_safe('<script type="%s" src="%s?%s"></script>' % (type, staticfiles_storage.url(filename), params))
    else:
        return mark_safe('<script type="%s" src="%s"></script>' % (type, staticfiles_storage.url(filename)))


@register.simple_tag
def js(filename, type='text/javascript'):
    '''A simple shortcut to render a ``script`` tag to a static javascript file'''
    return javascript(filename, type=type)


@register.simple_tag
def coffeescript(filename):
    '''A simple shortcut to render a ``script`` tag to a static coffeescript file'''
    return javascript(filename, type='text/coffeescript')


@register.simple_tag
def coffee(filename):
    '''A simple shortcut to render a ``script`` tag to a static coffeescript file'''
    return javascript(filename, type='text/coffeescript')


@register.simple_tag
def css(filename):
    '''A simple shortcut to render a ``link`` tag to a static CSS file'''
    return '<link rel="stylesheet" type="text/css" href="%s" />' % staticfiles_storage.url(filename)


def _boolean(value):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value.lower() == 'true'
    elif isinstance(value, int):
        return value != 0
    else:
        return False


@register.simple_tag
def jquery_js(version=None, migrate=False):
    '''A shortcut to render a ``script`` tag for the packaged jQuery'''
    version = version or settings.JQUERY_VERSION
    suffix = '.min' if not settings.DEBUG else ''
    libs = [js_lib('jquery-%s%s.js' % (version, suffix))]
    if _boolean(migrate):
        libs.append(js_lib('jquery-migrate-%s%s.js' % (JQUERY_MIGRATE_VERSION, suffix)))
    return '\n'.join(libs)


@register.inclusion_tag('djangojs/django_js_tag.html', takes_context=True)
def django_js(context, jquery=True, i18n=True, csrf=True, init=True):
    '''Include Django.js javascript library in the page'''
    return {
        'js': {
            'minified': not settings.DEBUG,
            'jquery': _boolean(jquery),
            'i18n': _boolean(i18n),
            'csrf': _boolean(csrf),
            'init': _boolean(init),
        }
    }


@register.inclusion_tag('djangojs/django_js_init.html', takes_context=True)
def django_js_init(context, jquery=False, i18n=True, csrf=True, init=True):
    '''Include Django.js javascript library initialization in the page'''
    return {
        'js': {
            'jquery': _boolean(jquery),
            'i18n': _boolean(i18n),
            'csrf': _boolean(csrf),
            'init': _boolean(init),
        }
    }

"""
Test helpers for Comprehensive Theming.
"""

from functools import wraps

from mock import patch

from django.conf import settings
from django.test.utils import override_settings

import edxmako

from .core import comprehensive_theme_changes


def with_comp_theme(theme_dir):
    """
    A decorator to run a test with a particular comprehensive theme.

    Arguments:
        theme_dir (str): the full path to the theme directory to use.
            This will likely use `settings.REPO_ROOT` to get the full path.

    """
    changes = comprehensive_theme_changes(theme_dir)

    def _decorator(func):                       # pylint: disable=missing-docstring
        @wraps(func)
        def _decorated(*args, **kwargs):        # pylint: disable=missing-docstring
            with override_settings(COMP_THEME_DIR=theme_dir, **changes['settings']):
                with edxmako.save_lookups():
                    for template_dir in changes['mako_paths']:
                        edxmako.paths.add_lookup('main', template_dir, prepend=True)

                    return func(*args, **kwargs)
        return _decorated
    return _decorator


def with_is_edx_domain(is_edx_domain):
    """
    A decorator to run a test as if IS_EDX_DOMAIN is true or false.

    We are transitioning away from IS_EDX_DOMAIN and are moving toward an edX
    theme. This decorator changes both settings to let tests stay isolated
    from the details.

    Arguments:
        is_edx_domain (bool): are we an edX domain or not?

    """

    def _decorator(func):                       # pylint: disable=missing-docstring
        if is_edx_domain:
            func = with_comp_theme(settings.REPO_ROOT / "themes" / "edx.org")(func)
        func = patch.dict('django.conf.settings.FEATURES', {"IS_EDX_DOMAIN": is_edx_domain})(func)
        return func
    return _decorator



def dump_theming_info():
    import os, os.path
    for namespace, lookup in edxmako.LOOKUP.items():
        print "--- %s: %s" % (namespace, lookup.template_args['module_directory'])
        for directory in lookup.directories:
            print "  %s" % (directory,)

    print "="*80
    for dir, dirs, files in os.walk(settings.MAKO_MODULE_DIR):
        print "%s ----------------" % (dir,)
        for file in sorted(files):
            if file.endswith(".pyc"):
                continue
            with open(os.path.join(dir, file)) as f:
                bytes = len(f.read())
            print "    %s: %d" % (file, bytes)

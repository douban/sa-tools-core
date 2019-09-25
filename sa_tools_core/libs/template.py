#!/usr/bin/env python
# coding: utf-8

from mako.lookup import TemplateLookup

from sa_tools_core.consts import PROJECT_ROOT
from sa_tools_core.utils import to_unicode


TEMPLATES_DIR = PROJECT_ROOT + '/templates'
MAGIC_EMPTY_LINE_MARK = '|'
lookup = TemplateLookup(directories=[TEMPLATES_DIR],
                        input_encoding='utf8',
                        output_encoding='utf8',
                        encoding_errors='ignore')


def render(template_name, strip_empty_lines=True, **data):
    out = lookup.get_template(template_name).render(**data)
    # When using Python 3, the render() method will return a bytes object, if output_encoding is set. Otherwise it returns
    # a string.
    out = to_unicode(out)

    if strip_empty_lines:
        return '\n'.join([('' if i.strip() == MAGIC_EMPTY_LINE_MARK else i)
                         for i in out.splitlines() if i.strip()]) + '\n'
    else:
        return out


def render_notification(**kw):
    title = render('icinga/notification.mako',
                   fragment_type='title',
                   **kw)
    content = render('icinga/notification.mako',
                     fragment_type='content',
                     **kw)
    return title, content

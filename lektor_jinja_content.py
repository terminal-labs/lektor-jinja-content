# -*- coding: utf-8 -*-
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

from lektor.db import Page
from lektor.pluginsystem import Plugin

class JinjaContentPlugin(Plugin):
    name = 'lektor-jinja-content'
    description = u'Render content fields with Jinja2.'

    def jinjaify(self, pad, source, data, field):
        '''Process each content field as if it's Jinja with the normal Template Context.'''
        context = {}
        context['site'] = pad
        context['this'] = source
        context['alt'] = source.alt
        context['config'] = pad.config
        try:
            data = self.env.jinja_env.from_string(data).render(context)
        except TypeError: # Content is not a string or template. Skip it.
            pass
        except TemplateSyntaxError:
            raise
        return data

    def on_before_build(self, builder, build_state, source, prog, **extra):
        pad = builder.pad
        if isinstance(prog.source, Page): # skips non-page Records and Assets
            for field in prog.source._data.keys():
                data = prog.source._data.get(field)
                if data:
                    try: # E.g. for fields like Markdown. Not all types have `source`.
                        prog.source._data[field].source = self.jinjaify(pad, prog.source, data.source, field)
                    except AttributeError:
                        prog.source._data[field] = self.jinjaify(pad, prog.source, data, field)


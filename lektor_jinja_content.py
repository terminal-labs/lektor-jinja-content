# -*- coding: utf-8 -*-
import click
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

from lektor.pluginsystem import Plugin

class JinjaContentPlugin(Plugin):
    name = 'lektor-jinja-content'
    description = u'Render content fields with Jinja2.'

    def jinjaify(self, context, data, field):
        '''Process each content field as if it's Jinja.'''
        try:
            data = self.env.jinja_env.from_string(data).render(context)
        except TypeError: # Content is not a string or template. Skip it.
            pass
        except (TemplateSyntaxError, UndefinedError):
            click.secho("Warning, you have a Jinja2 error for "
                        "{} content field '{}'.\n"
                        "You likely didn't expect this content to be rendered by Jinja.\n"
                        "Fix this by making it valid Jinja, "
                        "escaping that section (e.g. with {{% raw %}}),\n"
                        "or by disabling this plugin {} for this section."
                        .format(context['this'].path, field, self.name), fg='red')
            raise
        return data

    def on_process_template_context(self, context, **extra):
        for field in context['this']._data.keys():
            data = context['this']._data.get(field)

            if data:
                try: # E.g. for fields like Markdown. Not all types have `source`.
                    context['this']._data[field].source = self.jinjaify(context, data.source, field)
                except AttributeError:
                    context['this']._data[field] = self.jinjaify(context, data, field)

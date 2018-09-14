# -*- coding: utf-8 -*-
from jinja2.exceptions import UndefinedError
from markupsafe import Markup

from lektor.pluginsystem import Plugin


class JinjaContentPlugin(Plugin):
    name = "lektor-jinja-content"
    description = u"Render content fields with Jinja2."

    def safe_hasattr(self, field_val, attr):
        try:
            return hasattr(field_val, attr)
        except UndefinedError:
            return None

    def render_as_jinja(self, context, data):
        try:
            data = self.env.jinja_env.from_string(data).render(context)
        except TypeError:  # Content is not a string or template. Skip it.
            pass
        return data

    def process_field(self, context, field):
        if self.safe_hasattr(field, "source"):  # Markdown
            field.source = self.render_as_jinja(context, field.source)
        elif type(field) == Markup:
            field = Markup(self.render_as_jinja(context, field))
        else:  # Assumed to be String-like.
            field = self.render_as_jinja(context, field)
        return field

    def process_blocks(self, context, blocks):
        for idx, block in enumerate(blocks):
            for field in block:
                if self.safe_hasattr(block[field], "_blocks"):  #  Recurse
                    blocks[idx][field]._blocks = self.process_blocks(
                        context, blocks[idx][field]._blocks
                    )
                else:
                    blocks[idx][field] = self.process_field(context, blocks[idx][field])
        return blocks

    def on_process_template_context(self, context, **extra):
        # Only be triggered by page evaluation with _data attibute.
        if not extra["template"] or not hasattr(context["this"], "_data"):
            return

        for field in context["this"]._data.keys():
            field_val = context["this"]._data.get(field)
            if self.safe_hasattr(field_val, "_blocks"):
                context["this"]._data[field]._blocks = self.process_blocks(
                    context, context["this"]._data[field]._blocks
                )
            else:
                context["this"]._data[field] = self.process_field(
                    context, context["this"]._data[field]
                )

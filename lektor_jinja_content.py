# -*- coding: utf-8 -*-
import traceback
from jinja2.exceptions import UndefinedError
from markupsafe import Markup

from lektor.markdown import Markdown
from lektor.pluginsystem import Plugin
from lektor.types.flow import Flow, FlowBlock, FlowDescriptor
from lektor.types.formats import MarkdownDescriptor
from lektor.utils import Url

class JinjaContentPlugin(Plugin):
    name = "lektor-jinja-content"
    description = u"Render content fields with Jinja2."

    def render_as_jinja(self, data):
        try:
            return self.env.jinja_env.from_string(data).render(self.context)
        except TypeError:  # Content is not a string or template. Skip it.
            pass

    def process_field(self, field, field_data):
        if isinstance(field_data, MarkdownDescriptor):
            self.this._bound_data[field] = field_data.__get__(self.this)
            self.this._bound_data[field].source = self.render_as_jinja(field_data.source)
        elif isinstance(field_data, Markup):
            self.this._bound_data[field] = Markup(self.render_as_jinja(context, field_data))
        elif isinstance(field_data, property):
            self.this._bound_data[field] = self.render_as_jinja(
                field_data.__get__(self.this)
            )
        elif isinstance(field_data, list):
            self.this._bound_data[field] = [self.render_as_jinja(datum) for datum in field_data]
        elif isinstance(field_data, str):
            self.this._bound_data[field] = self.render_as_jinja(field_data)

    def process_block_item(self, block, field):
        if isinstance(block[field], FlowDescriptor):
            self.process_flow_descriptor(block[field])
        if isinstance(block[field], MarkdownDescriptor):
            block[field].source = self.render_as_jinja(block[field].source)
        elif isinstance(block[field], str):
            block[field] = self.render_as_jinja(block[field])

    def process_flow_descriptor(self, flow_descriptor):
        for block in flow_descriptor._blocks:
            for block_field in block:
                self.process_block_item(block, block_field)

    def on_process_template_context(self, context, **extra):
        # Only be triggered by page evaluation with _data attibute.
        self.context = context

        if 'this' not in context or not hasattr(context['this'], "_data"):
            return

        self.this = context['this']

        for field in self.this.datamodel.field_map:
            field_data = self.this._data[field]
            if isinstance(field_data, FlowDescriptor):
                self.process_flow_descriptor(field_data)
            else:
                self.process_field(field, field_data)

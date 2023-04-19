# -*- coding: utf-8 -*-
import datetime
from numbers import Number

from markupsafe import Markup

from lektor.pluginsystem import Plugin
from lektor.types.flow import FlowDescriptor
from lektor.types.formats import MarkdownDescriptor


class JinjaContentPlugin(Plugin):
    name = "lektor-jinja-content"
    description = "Render content fields with Jinja2."

    def render(self, data):
        """Return data rendered as jinja, and ignore type incompatibilities."""
        try:
            return self.env.jinja_env.from_string(data).render(self.context)
        except TypeError:  # Content is not a string or template. Skip it.
            pass

    def process_field(self, field, field_data):
        """Calculate and set the _bound_data for a field on a page."""
        if not field_data:
            return

        if isinstance(field_data, MarkdownDescriptor):
            self.bound_data[field] = field_data.__get__(self.this)
            self.bound_data[field].source = self.render(field_data.source)
        elif isinstance(field_data, Markup):
            self.bound_data[field] = Markup(self.render(field_data))
        elif isinstance(field_data, property):
            self.bound_data[field] = self.render(field_data.__get__(self.this))
        elif isinstance(field_data, list):
            self.bound_data[field] = [self.render(datum) for datum in field_data]
        elif not isinstance(
            field_data, (Number, datetime.date)  # Should we avoid anything else?
        ):
            self.bound_data[field] = self.render(field_data)

    def process_block_item(self, block, field):
        """Calculate and set the _bound_data for a field in a block.
        Recurse if a field is another flow block.
        """
        if isinstance(block[field], FlowDescriptor):
            self.process_flow_descriptor(block[field])
        if isinstance(block[field], MarkdownDescriptor):
            block[field].source = self.render(block[field].source)
        elif isinstance(block[field], str):
            block[field] = self.render(block[field])

    def process_flow_descriptor(self, flow_descriptor):
        """Loop through all fields in all blocks of a flowblock and initiate
        rendering their values as jinja.
        """
        for block in flow_descriptor._blocks:
            for block_field in block:
                self.process_block_item(block, block_field)

    def on_process_template_context(self, context, **extra):
        """Loop through all fields in a page and initiate
        rendering their values as jinja.
        """
        # Only be triggered by page evaluation with _data attibute.
        if "this" not in context or not hasattr(context["this"], "_data"):
            return

        self.context = context
        self.this = context["this"]
        self.bound_data = self.this._bound_data

        for field in self.this.datamodel.field_map:
            field_data = self.this._data[field]
            if isinstance(field_data, FlowDescriptor):
                self.process_flow_descriptor(field_data)
            else:
                self.process_field(field, field_data)

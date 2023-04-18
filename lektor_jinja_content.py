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
    types = set()

    @staticmethod
    def get_data(this, field):
        """Lektor's record getitem does some thinking for us that is actually some,
        trouble for us, so use our own method to get data, sometimes transformed
        by an underlying __get__, but don't get the _bound_data.
        """
        # if isinstance(field, MarkdownDescriptor):
        #     breakpoint()
        rv = this._data[field]
        if hasattr(rv, "__get__"):
            rv = rv.__get__(this)
        # Don't modify anything, just get!
        # if isinstance(this, FlowBlock):

        # if hasattr(this, 'path') and "clientele" in this.path and field=='body':
        #     breakpoint()
        return rv

    @staticmethod
    def safe_hasattr(field_val, attr):
        try:
            return hasattr(field_val, attr)
        except UndefinedError:
            return None

    def render_as_jinja(self, context, data):
        try:
            return self.env.jinja_env.from_string(data).render(context)
        # except:
        #     breakpoint()
        #     pass
        except TypeError:  # Content is not a string or template. Skip it.
            pass
        # except Exception as e:
        #     breakpoint()
        #     pass

    def process(self, context, field, recursive=False):
        print(f"{recursive=}")
        if recursive: # isinstance(field, Flow):
            # breakpoint()
            pass
        if isinstance(field, Flow):
            return self.process_blocks(context, field, recursive)
        return self.process_value(context, field, recursive)

    def process_value(self, context, val, recursive=False):
        # if recursive:
        #     breakpoint()
        if self.safe_hasattr(val, "source"):  # Markdown
            val.source = self.render_as_jinja(context, val.source)
        elif type(val) == Markup:
            val = Markup(self.render_as_jinja(context, val))
        elif isinstance(val, str):  # Assumed to be String-like.
            val = self.render_as_jinja(context, val)
        elif isinstance(val, list):
            val = [self.render_as_jinja(context, val) for val in val]
        else:
            return val
        return val

    def process_field(self, context, this, field, field_data):
        if isinstance(field_data, MarkdownDescriptor):
            this._bound_data[field] = field_data.__get__(this)
            this._bound_data[field].source = self.render_as_jinja(context, field_data.source)
        elif isinstance(field_data, property):
            this._bound_data[field] = self.render_as_jinja(
                context, field_data.__get__(this)
            )
        elif isinstance(field_data, str):
            this._bound_data[field] = self.render_as_jinja(context, field_data)

    def on_process_template_context(self, context, **extra):
        # Only be triggered by page evaluation with _data attibute.
        self.context = context

        if 'this' not in context or not hasattr(context['this'], "_data"):
            return

        self.this = context['this']

        def process_block_item(block, field):
            if isinstance(block[field], FlowDescriptor):
                process_flow_descriptor(block[field])
            if isinstance(block[field], MarkdownDescriptor):
                block[field].source = self.render_as_jinja(self.context, block[field].source)
            elif isinstance(block[field], str):
                block[field] = self.render_as_jinja(self.context, block[field])

        def process_flow_descriptor(flowd):
            for block in flowd._blocks:
                for block_field in block:
                    process_block_item(block, block_field)

        for field in self.this.datamodel.field_map:
            field_data = self.this._data[field]
            if isinstance(field_data, FlowDescriptor):
                process_flow_descriptor(field_data)
            else:
                self.process_field(self.context, self.this, field, field_data)

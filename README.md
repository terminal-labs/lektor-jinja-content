# lektor-jinja-content

[![Build Status](https://api.travis-ci.org/terminal-labs/lektor-jinja-content.svg?branch=master)](https://travis-ci.org//terminal-labs/lektor-jinja-content)
[![Code Coverage](https://codecov.io/gh/terminal-labs/lektor-jinja-content/branch/master/graph/badge.svg)](https://codecov.io/gh//terminal-labs/lektor-jinja-content)
[![PyPI version](https://badge.fury.io/py/lektor-jinja-content.svg)](https://pypi.org/project/lektor-jinja-content/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lektor-jinja-content.svg)](https://pypi.org/project/lektor-jinja-content/)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

This is a Lektor plugin that allows you to render Jinja2 inside your content fields that are string-like. For example, this means that inside your content fields that are of type string or Markdown, you can write Jinja logic, and access Lektor's [Template Context](https://www.getlektor.com/docs/templates/#template-context), and has access to all normal Jinja filters, including those provided by [other plugins](https://github.com/terminal-labs/lektor-slugify). In a Markdown field (or other field that is rendered - like [rst](https://github.com/fschulze/lektor-rst)), the **Jinja is processed first**, then the formatting processor.

You can set and use Jinja variables, but they will only have meaning within their field that is being rendered.

With this plugin, you'll have to make sure the content that is rendered **is valid Jinja**. Jinja syntax erros will throw an exception. Don't forget about the handy `{% raw %} {% endraw %}` tags if you want content that is not valid Jinja.

**N.B.** Using this plugin is rendering many more items with Jinja, and your build process will slow down as a result. As an early benchmark and anecdote, my small website's build time rose from 4.89s to 5.39s even while I actually had no Jinja-Content that needed rendering. I plan on adding the ability to configure this plugin later so that you don't have to run *everything* through Jinja if you don't want to.


## Examples

Querying context: `{{ site.get('/').title }}` or `{{ this.path }}`

Logic:
```jinja
{% set meaning_of_life, meaning_of_universe = this.life, this.universe %}
{% if meaning_of_life == meaning_of_universe == 42 %}
  {% set meaning_of_it_all = meaning_of_life %}
{% else %}
  {% set meaning_of_it_all = 'Undefined' %}
{% endif %}
{{ meaning_of_it_all }}
```

Jinja in Markdown:
```jinja
[link text]({{ this|url }})
```

Jinja in reStructuredText:
```jinja
`link text <{{ this|url }}>`_
```

Try running the [test site](https://github.com/terminal-labs/lektor-jinja-content/blob/master/tests/demo-project/) for more examples.


## Possible future of this plugin.

This Plugin opens the door to some pretty powerful and pretty funky functionality. Here's some food for though:

* Currently every every string-like field in `_data` and `_blocks` is processed, even things like `_slug` and `_template`. Can these other things be used?
* [Some people want to be able to include markdown in content files / declarations](https://github.com/lektor/lektor/issues/541). This plugin might pave the way toward that with [includes and extends](https://github.com/terminal-labs/lektor-jinja-content/issues/3).
* Could we Jinjaify static files?
* [Databags?](https://github.com/terminal-labs/lektor-jinja-content/issues/4)
* [What about modularity?](https://github.com/terminal-labs/lektor-jinja-content/issues/2)

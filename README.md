# lektor-jinja-content

This is a Lektor plugin that allows you to render Jinja2 inside your content fields that are string-like. For example, this means that inside your content fields that are of type string or Markdown, you can write Jinja logic, and access Lektor's [Template Context](https://www.getlektor.com/docs/templates/#template-context), and has access to all normal Jinja filters, including those provided by [other plugins](https://github.com/terminal-labs/lektor-slugify). In a Markdown field (or other field that is rendered - like [rst](https://github.com/fschulze/lektor-rst)), the **Jinja is processed first**, then the formatting processor.

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

# lektor-jinja-content

This is a Lektor plugin that allows you to render jinja inside your content fields that are string-like. For example, this means that inside your content fields that are of type string or Markdown, you can write jinja logic, and access Lektor's [Template Context](https://www.getlektor.com/docs/templates/#template-context).

Querying context:
- `{{ site }}`
- `{{ this }}`

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

*N.B.* Using this plugin is rendering many more items with Jinja, and your build process will slow down with this. As an early benchmark and anecdote, my small website's build time rose from 4.89s to 5.39s even while I actually had no Jinja-Content that needed rendering. I plan on adding the ability to configure this plugin later so that you don't have to run *everything* through Jinja if you don't want to.

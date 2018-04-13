# lektor-jinja-content

This is a Lektor plugin that provides allows you to render jinja inside your content fields that are string-like. For example, this means that inside your content fields that are of type string or Markdown, you can write jinja logic, and access Lektor's [Template Context](https://www.getlektor.com/docs/templates/#template-context).

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

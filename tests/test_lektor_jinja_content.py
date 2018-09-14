import os

root_positive_strings = [
    "<p>In Jinja!",
    "<p>this.path = /</p>",
    "page_num",
    "_bound_data",
    "_data",
    "'IMAGEMAGICK_EXECUTABLE': None",
    "<p>alt = _primary</p>",
    "<p>math = 2 + 2 = 4</p>",
    "<b>{% if True %}~raw~{% endif %}</b>",
    "<li>Jinja Content</li>",
    "<li>aCeiJjnnnott</li>",
    "This is in a nested flowblock.",
]

root_negative_strings = ["False!", "{% raw %}", "{% endraw %}", "Not visible!", "{{"]


def test_builder(pad, builder):
    failures = builder.build_all()
    assert not failures
    root_path = os.path.join(builder.destination_path, "index.html")
    with open(root_path) as root_file:
        root_html = root_file.read()

    for string in root_positive_strings:
        assert string in root_html

    for string in root_negative_strings:
        assert string not in root_html

    # lektor-tags compatibility
    tag_path = os.path.join(builder.destination_path, "tag/index.html")
    with open(tag_path) as tag_file:
        tag_html = tag_file.read()
    subpage_path = os.path.join(builder.destination_path, "subpage/index.html")
    with open(subpage_path) as subpage_file:
        subpage_html = subpage_file.read()

    assert '<li><a href="../subpage/">subpage</a></li>' in tag_html
    assert '<a href="../tag">' in subpage_html

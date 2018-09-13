import os

test_strings = [
    "<p>In Jinja!",
    "<p>this = /</p>",
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


def test_builder(pad, builder):
    failures = builder.build_all()
    assert not failures
    page_path = os.path.join(builder.destination_path, "index.html")
    html = open(page_path).read()

    for string in test_strings:
        assert string in html

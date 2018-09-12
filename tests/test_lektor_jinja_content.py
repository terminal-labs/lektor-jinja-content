import os

import flask
from lektor.context import Context

app = flask.Flask(__name__)


def test_builder(pad, builder):
    failures = builder.build_all()
    assert not failures

    def get_page(tag):
        path = os.path.join(builder.destination_path,
                            'blog/tag/%s/index.html' % tag)

        return open(path).read().strip()

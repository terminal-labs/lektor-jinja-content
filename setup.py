from setuptools import setup

setup(
    name='lektor-jinja-content',
    version='0.1',
    author='Terminal Labs, Joseph Nix',
    author_email='solutions@terminallabs.com',
    url='https://github.com/terminal-labs/lektor-jinja-content',
    description = u'Render content fields with Jinja2.',
    license='BSD-3-Clause',
    py_modules=['lektor_jinja_content'],
    entry_points={
        'lektor.plugins': [
            'jinja-content = lektor_jinja_content:JinjaContentPlugin',
        ]
    }
)

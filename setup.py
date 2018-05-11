import ast
import io
import re

from setuptools import setup

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_jinja_content.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='Terminal Labs, Joseph Nix',
    author_email='solutions@terminallabs.com',
    description=description,
    keywords='Lektor plugin static-site jinja jinja2',
    license='BSD-3-Clause',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-jinja-content',
    py_modules=['lektor_jinja_content'],
    url='https://github.com/terminal-labs/lektor-jinja-content',
    version='0.3',
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Lektor',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'lektor.plugins': [
            'jinja-content = lektor_jinja_content:JinjaContentPlugin',
        ]
    }
)

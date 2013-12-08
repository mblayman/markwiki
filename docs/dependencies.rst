Dependencies
============

This page documents information about the dependencies used in MarkWiki.

setup.py
--------

MarkWiki includes some ``setup_requires`` dependencies. These are needed to
execute the test suite via ``python setup.py nosetests``.

The dependencies included in ``install_requires`` are the *logical*
dependencies that MarkWiki requires. This list captures what is needed to run
MarkWiki, but not which specific versions.

requirements.txt
----------------

The list of dependencies in ``requirements.txt`` are the actual versions that
MarkWiki was tested with. This list captures extra information about
dependencies of dependencies as well.

Rationale
---------

Each dependency serves a certain purpose. The following describes why each
tool in ``setup.py`` was selected.

* **argparse** - Used to provide the argument parsing module for any
  installation of MarkWiki using Python 2.6.
* **Flask** - MarkWiki is a web application built on top of the Flask web
  application framework. Flask is core to the operation of MarkWiki.
* **Flask-Login** - This Flask extension creates the capability to handle
  logged in users.
* **Flask-WTF** - This Flask extension is used for creating HTML forms via
  WTForms.
* **Frozen-Flask** - The ability to generate a static version of a MarkWiki
  comes from this Flask extension.
* **Markdown** - All Markdown pages are transformed into HTML from this
  dependency.
* **Pygments** - Code syntax highlighting is provided by Pygments.
* **Whoosh** - This is the search tool used by MarkWiki.

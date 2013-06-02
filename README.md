MarkWiki
========

*A simple wiki using Markdown*

The user documentation for MarkWiki is at http://pythonhosted.org/MarkWiki/.

Running MarkWiki
----------------

### Users

From a command line, run:

```bash
$ pip install MarkWiki
$ markwiki
```

### Developers

From the project's root directory, run:

```bash
$ python setup.py develop
$ markwiki
```

Design Goal
-----------

MarkWiki should be as simple as possible to set up. A basic working
configuration should never need more than two steps.

1.  Install the dependencies.
2.  Start the web server.

Why? MarkWiki is aimed at teams that want a no fuss, no frills wiki. Simplicity
trumps features.

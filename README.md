MarkWiki
========

*A simple wiki using Markdown*

The user documentation for MarkWiki is at http://pythonhosted.org/MarkWiki/.

Design Goal
-----------

MarkWiki should be as simple as possible to set up. A basic working
configuration should never need more than two steps.

1.  Install the dependencies.
2.  Start the web server.

Why? MarkWiki is aimed at teams that want a no fuss, no frills wiki. Simplicity
trumps features.

Contributing
------------

Fork MarkWiki on GitHub and submit a pull request when you're ready.

Guidelines:

1. Your code should follow PEP 8 style. Run it through `pep8` to check.
2. Please try to conform with any other conventions seen in the code for
   consistency (e.g., using ''' for docstrings instead of """).
3. Make sure your change works against master! (Bonus points for unit tests.)

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

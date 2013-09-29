MarkWiki Features
=================

MarkWiki stays very true to the [original Markdown specification] [syn] with
some minor deviations. It also has other cool features that make working
with Markdown even better!

[TOC]

### Wiki Links

Normal Markdown syntax does not include wiki links, but MarkWiki does. Text
between open and closing double square brackets will be treated as a wiki link.
`[[AnAwesomeWikiPage]]` is an example of a valid wiki link.

Wiki links can include letters, numbers, dashes, underscores, spaces, and
forward slashes.

If you ever need to use a literal \[\[ for some reason, you can use a backslash
(\\) immediately before each square bracket. This will prevent MarkWiki
from turning it into a wiki link.

### Authentication

By default, MarkWiki lets any anonymous user edit (and delete!) whatever they
want. This enables teams to start up quickly if they do not care about
controlling access.

Some teams, however, would like to reduce the number of people who can edit
the wiki, so MarkWiki makes it easier to enable user identification. When
authentication is enabled, only logged in users will be able to create, edit,
and delete wiki pages. See [[MarkWiki/Settings]] for more information.

### Wiki Sections

A forward slash in a wiki link is used to group pages. MarkWiki takes advantage
of this categorization itself by putting all its help pages under the
`MarkWiki` category. This documentation generally refers to these categories as
"Sections." Sections can exist within other sections and can be as deep as
desired, but it is recommended that you [[Please/Do/Not/Torture/Others]].

### Table Of Contents

You can add a table of contents anywhere in the wiki page by putting `[TOC]` on
a line by itself. This page has an example if you look at the Markdown source.

### Code Highlighting

MarkWiki supports code blocks in traditional Markdown style (i.e. by using
identation). MarkWiki also supports a code block style similar to
[GitHub] [git]. You can create a code block by using triple backticks (\`\`\`)
at the beginning of a line and closing the block with more triple backticks.

    ```
    <Your code here>
    ```

This technique can also be used to highlight code if you provide the language
after the first set of backticks. Check the source of this help page and look
at the example below.

```python
class Foo(object):
    '''This is a Python documentation string.'''

    def __init__(self, bar):
        self.bar = bar

```

### Freezing

In some scenarios, you may not be able to run a web server that is able to run
MarkWiki, but you need to publish a readable version of your wiki. For that,
you can freeze your wiki to take a snapshot of the content. It's exactly how
the [MarkWiki documentation] [docs] is hosted on `http://pythonhosted.org`. To
freeze your wiki, run:

```bash
$ markwiki -f "<destination>"
```

In the example, `<destination>` is the directory that you want the frozen wiki
to be stored.

### Customization

MarkWiki provides a method to completely customize the interface through use of
the `STATIC_PATH` and `TEMPLATE_PATH` settings. By using these settings, an
intrepid user can create all new themes and structure for MarkWiki's pages.
Check out `Advanced Settings` in [[MarkWiki/Settings]] for more.

[syn]: http://daringfireball.net/projects/markdown/syntax
[git]: https://github.com
[docs]: http://pythonhosted.org/MarkWiki/

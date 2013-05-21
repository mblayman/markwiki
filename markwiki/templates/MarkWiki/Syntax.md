Writing In MarkWiki
===================

MarkWiki stays very true to the [original Markdown specification] [syn] with
some minor deviations.

### Wiki Links

Normal Markdown syntax does not include wiki links, but MarkWiki does. Text
between open and closing double square brackets will be treated as a wiki link.
`[[AnAwesomeWikiPage]]` is an example of a valid wiki link.

Wiki links can include letters, numbers, dashes, underscores, spaces, and
forward slashes.

A forward slash is used to group pages. MarkWiki takes advantage of this
categorization itself by putting all its help pages under the `MarkWiki`
category.

If you ever need to use a literal \[\[ for some reason, you can use a backslash
(\\) immediately before each square bracket. This will prevent MarkWiki
from turning it into a wiki link.

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

[syn]: http://daringfireball.net/projects/markdown/syntax
[git]: https://github.com


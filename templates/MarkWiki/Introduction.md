Welcome to MarkWiki
===================

> MarkWiki is a wiki that uses Markdown to create pages. Markdown has a simple
text based approach to define content which you can [learn very quickly] [syn].

### Why Should I Use MarkWiki?

The aim of MarkWiki is to be dead simple. MarkWiki was born out of frustration
with bad documentation tools behind a company firewall.

You should consider MarkWiki if you:

* Need something working fast.
* Are looking for a no fuss answer to how to collaborate with teammates.

### Getting Started

If you've made it this far, then you've probably figured out how to run
MarkWiki. Congratulations! Now you may want to consider a bit more
configuration so you don't have to restart MarkWiki manually every time your
server reboots. Check out [[MarkWiki/Deployment]].

You might, however, be reading this from some other website. MarkWiki
requires a few steps to get going. Fire up the command line and follow along!

1. Download it. (TODO: Provide a place to download.)
2. Install it.
3. Run the built-in web server.

```bash
$ pip install -r requirements.txt
$ python markwiki.py
```

### Now What?

You can begin by editing this page to suit your needs (don't worry, a copy of
this page can be found at [[MarkWiki/Introduction]] if you ever need to refer
back).

There are a couple of things that MarkWiki does differently than Markdown. The
most obvious one is that we support internal wiki pages. You can make a wiki
page by surrounding a path in double square brackets (e.g., \[[MyCoolPage]]).
Other differences can be found by checking out [[MarkWiki/Syntax]].

[syn]: http://daringfireball.net/projects/markdown/syntax


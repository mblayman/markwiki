Settings
========

The settings that are unique to MarkWiki or are used internally by MarkWiki
are listed below.

To override default settings, you will need to create a configuration file and
set an environment variable named `MARKWIKI_SETTINGS` with the path of that
configuration file. MarkWiki will read the settings when it starts.

```bash
$ export MARKWIKI_SETTINGS="/home/matt/production.config"
$ markwiki
```

[A sample production configuration file is available.] [prod]

### MarkWiki Specific Settings

### Flask Settings Used By MarkWiki

TODO: Document them all.

TODO: Make a production sample.
[prod]: https://raw.github.com/mblayman/markwiki/master/production.config

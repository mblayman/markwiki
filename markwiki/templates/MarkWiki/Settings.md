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

The default settings are geared toward development so please be sure to check
the settings before putting MarkWiki into production. Be safe, folks.

### MarkWiki Specific Settings

* `SERVER_HOST` - This is the hostname of the server. Defaults to `0.0.0.0`.
* `SERVER_PORT` - This is the port number used by the server. Defaults to
  `5000`.
* `WIKI_PATH` - This is the location where all of MarkWiki's content is
  stored. Defaults to `~/.markwiki`.

### Flask Settings Used By MarkWiki

* `DEBUG` - This is a debug flag. It is ***VERY IMPORTANT*** that this be set
  to `False` for a production environment. Otherwise bad guys may find ways
  to exploit your server. Defaults to `True`.
* `SECRET_KEY` - This is used to provide security for user session data. Please
  be sure to select something unique and very hard to guess. Defaults to `It's
  a secret to everybody.`.

[prod]: https://raw.github.com/mblayman/markwiki/master/production.config

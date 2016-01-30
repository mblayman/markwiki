Settings
========

[TOC]

The settings that are unique to MarkWiki or are used internally by MarkWiki
are listed below.

To override default settings, you will need to create a configuration file and
set an environment variable named `MARKWIKI_SETTINGS` with the path of that
configuration file. MarkWiki will read the settings when it starts.

MarkWiki will also take any settings from environment variables if they are
defined. Environment variables will override default settings or any settings
from a configuration file.

```bash
$ export MARKWIKI_SETTINGS="/home/matt/production.config"
$ markwiki
```

[A sample production configuration file is available.] [prod]

The default settings are geared toward development so please be sure to check
the settings before putting MarkWiki into production. Be safe, folks.

### MarkWiki Specific Settings

*   `MARKWIKI_HOME` - This is the location where all of MarkWiki's content is
    stored.

    Defaults to `~/.markwiki`.

*   `AUTHENTICATION` - This determines if any form of authentication will be
    used by MarkWiki. The authentication type should be `'basic'` if
    authentication is to be used. MarkWiki does *not* configure SSL
    certificates for secure browsing.

    If MarkWiki is not proxied behind a server configured to use HTTPS then
    credentials will be passed to the server in plain text!

    Defaults to `None`.

*   `ADMINISTRATOR` - This is the username of the account that will have
    administrative privileges if authentication is enabled. The adminstrator
    has the ability to create new user accounts.

    Defaults to `None`.

*   `ADMIN_PASSWORD` - This is the password for the administrator account.

    Defaults to `None`.

*   `ALLOW_REGISTRATION` - This sets whether or not new users will be able to
    register an account themselves when authentication is enabled. If `False`,
    an administrator must create new accounts.

    Defaults to `True`.

*   `SERVER_HOST` - This is the hostname of the server.

    Defaults to `0.0.0.0`.

*   `SERVER_PORT` - This is the port number used by the server.

    Defaults to `5000`.

*   `STORAGE_TYPE` - MarkWiki is designed to store its data in multiple
    possible formats. The currently supported formats are: 'file'.

    Defaults to `file`.

*   `GIT_ENABLED` - This allows to use a local git repository to version
    the pages of the wiki. It also then allows to view and revert a page
    to any old version if needed.

    Defaults to `False`.

### Flask Settings Used By MarkWiki

*   `DEBUG` - This is a debug flag. It is ***VERY IMPORTANT*** that this be set
    to `False` for a production environment. Otherwise bad guys may find ways
    to exploit your server.

    Defaults to `False`.

*   `SECRET_KEY` - This is used to provide security for user session data.
    Please be sure to select something unique and very hard to guess.

    Defaults to `It's a secret to everybody.`.

### Advanced Settings

*   `STATIC_PATH` - This is to override the path to static files (like
    JavaScript and CSS). It can be used to customize the user interface.

    Defaults to `None` to use the default interface.

*   `TEMPLATE_PATH` - This is to override the path to template files that
    provide the structure of the pages. It can be used to customize the user
    interface.

    Defaults to `None` to use the default interface.

[prod]: https://raw.github.com/mblayman/markwiki/master/production.config

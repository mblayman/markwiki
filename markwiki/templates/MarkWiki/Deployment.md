Deploying MarkWiki
==================

So you're past the evaluation period and ready to make MarkWiki more permanent?
Great, let's get you going.

MarkWiki is built on top of a web framework called Flask. This is unimportant
except that the authors of Flask have great documentation on how to deploy
Flask applications. Since MarkWiki is a Flask app, this documentation applies
to MarkWiki so [check out the Flask deployment docs] [flask].

There are also different setting that a system administrator will want to set
for MarkWiki. All the settings are documented on the [[MarkWiki/Settings]]
page.

### An Example With Nginx

[Nginx] [nginx] is a popular web server to use when deploying to production
environments. This section will attempt to provide a realistic deployment
example using MarkWiki and Nginx (via uWSGI). This is to help those that might
get confused by the somewhat unspecific examples listed in the Flask
documentation.

Now, here is a bit of context. MarkWiki is a [WSGI] [wsgi] application.
[uWSGI] [uwsgi] is software that can run WSGI application very quickly. Nginx
will talk to uWSGI to get web data from MarkWiki.

This sample configuration was done with Ubuntu 12.04. There may be differences
in what is required to set up MarkWiki for your particular environment.

First, install Nginx, uWSGI, and the uWSGI Python plugin. The Python
development package is included so that some of MarkWiki's dependencies can
include some optional speed-ups. Also, install pip.

With the necessary Ubuntu packages installed, install MarkWiki.

```bash
$ sudo apt-get install nginx uwsgi uwsgi-plugin-python python-dev python-pip
$ sudo pip install MarkWiki
```

By default, Nginx will be configured to start automatically on reboot, but for
first time use, start it.

```bash
$ sudo service nginx start
```

Run:
```bash
$ uwsgi --plugin python --http :9090 --module markwiki --callable app
```

*TODO*: There is more to show:

*   uWSGI is still not hooked into Nginx. MarkWiki is visible locally on 9090
    but 80 or 443 are still high and dry. :(
*   Does Flask need any modifications for proxies? Investigating...
*   How does uWSGI survive restarts? init.d script? upstart? supervisord? Lots
    of potential options to explore.
*   Show SSL setup for authentication support? That would be nice.

** *TODO:* I promise I'll try to finish the example here. In the interim, you
may have some success with [the uWSGI quickstart] [uwsgitut].**

[flask]: http://flask.pocoo.org/docs/deploying/#deployment
[nginx]: http://wiki.nginx.org/Main
[wsgi]: http://wsgi.readthedocs.org/en/latest/
[uwsgi]: http://uwsgi-docs.readthedocs.org/en/latest/
[uwsgitut]: http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html


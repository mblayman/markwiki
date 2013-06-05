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
example using MarkWiki and Nginx. This is to help those that might get confused
by the somewhat unspecific examples listed in the Flask documentation.

** *TODO:* I promise I'll try to get a good example here.**

[flask]: http://flask.pocoo.org/docs/deploying/#deployment
[nginx]: http://wiki.nginx.org/Main


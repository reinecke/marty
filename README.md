Marty
=====

A bot for [Slack](https://slack.com/) because [Marty](http://www.imdb.com/character/ch0001829/?ref_=tt_cl_t1) is... [a slacker](http://www.imdb.com/title/tt0088763/quotes?item=qt0416359)

What does it do?
=============
Right now, the only thing it does is generate memes for you and post them in the channel you ran the command from.

Do something like:

`/meme fry "Not sure if easy meme creation is good" "or just wasting lives"`

And a few seconds the bot should post an image like:

![Futurama Fry Meme](http://cdn.meme.am/instances/300x/54615053.jpg)

You can also do something like:

`/meme "sudden clarity clarence"`

To simply post the background image without it's text.

Project Status
===========
This project is in very early stages. I posted it sooner than later so that we can all work on it together!
Pull requests are awesome!

Dependencies
===========
- flask
- requests

Installation
========
First, update config.py with your settings:
```python
client_id = "SLACK CLIENT ID"
client_secret = "SLACK CLIENT SECRET"
token = "SLACK UNIVERSAL ACCESS TOKEN"
name = "Marty"
imgur_id = 'IMGUR APP ID'
imgur_secret = 'IMGUR APP SECRET'
memegen_username = 'MEMEGEN.NET USERNAME'
memegen_password = 'MEMEGEN.NET PASSWORD'
```

Right now, all that is actually used from config is `token`, `memegen_username`, and `memegen_password`. As more functionality is added I'll likely use more of the config settings.

Consult your hosting provider on how to deploy flask apps.

The app itself should be importable doing something like:

```python
from marty import app as application
```

Then, go to api.slack.com and create a new slack access token (this is under "Authentication") toward the bottom of the page.
The token issued by this is what you'll use as the token in the config.

Finally, in the integrations section of your slack team panel, add a Slash Command (/meme), and point it at the www.serverwhereyourunthemartyflaskapp.com/command endpoint using method POST. I also enabled showing the command in the autocomplete list with the following description and usage strings:

Makes a meme and posts it

[meme name] "top text" "bottom text"

That should be it!

Licensing
=======
Marty is provided under the MIT License


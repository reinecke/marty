from flask import Flask
from flask import abort
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import Response
from crossdomain import crossdomain

import json
import requests
import urlparse
import shlex

import config

import memegenerator_net

# Create the app instance
app = Flask(__name__)

PORT = 8686

BASE_URL = "https://slack.com/api/"

class SlackError():pass

def _scrub_slack_text(text):
    '''
    does minimal escaping as dictated by:
    https://api.slack.com/docs/formatting
    '''
    
    return text.replace('&', '&amp;').replace('<','&lt;').replace('<', '&gt;')

def send_message(channel, text, as_user=None):
    if not as_user:
        as_user = "Marty"
    payload = {'username': as_user, 
            'text': text,
            'token': config.token,
            'channel': channel}
    url = urlparse.urljoin(BASE_URL, 'chat.postMessage')
    response = requests.post(url, data=payload, verify=False)
    
    json_response = response.json()
    if not json_response.get('ok'):
        raise SlackError(json_response.get('error'))

def make_meme(request):
    # parse the command
    text = request.form.get('text')
    usage = _scrub_slack_text('You must provide something like: winter is coming "top text" "bottom text"')
    if not text:
        return usage

    # Parse the desired meme info
    args = shlex.split(text)
    if len(args) == 2 or not args:
        return usage
    
    # If only one arg, fetch the meme image only
    if len(args) == 1:
        meme_name = args[0]
        top_text = ''
        bottom_text = ''
    else:
        bottom_text = args[-1]
        top_text = args[-2]
        meme_name = ' '.join(args[:-2])
 
    # fetch the meme
    meme = memegenerator_net.get_meme(meme_name)
    
    if not meme:
        return _scrub_slack_text("Meme not found: "+str(meme_name))

    channel_id = request.form.get('channel_id')
    if not top_text.strip() and not bottom_text.strip():
        meme_url = meme['imageUrl']
    else:
        try:
            meme_url = memegenerator_net.create_meme(meme, 
                    [top_text, bottom_text])
        except memegenerator_net.MemeError, e:
            return _scrub_slack_text("Error creating meme: "+str(e))
    
    # Send the message to the channel
    from_user = request.form.get('user_name')
    try:
        send_message(channel_id, "<"+meme_url+">", as_user=from_user)
    except SlackError, e:
        return _scrub_slack_text("Error creating meme: "+str(e))
    
    return ''

COMMAND_DICT = {'/meme':make_meme}

@app.route("/")
def root_page():
    return Response("Nothing to see here :/")

@app.route("/auth")
def authorize():
    # TODO: Implement OAuth2
    return Respone("ok")

@app.route("/command", methods=["POST"])
@crossdomain(origin='*')
def command():
    '''
    Sample form data
    token=vJCya5BQ9phePIQ8ZwCAqagA
	team_id=T0001
	channel_id=C2147483705
	channel_name=test
	user_id=U2147483697
	user_name=Steve
	command=/weather
	text=94070
    '''
    # TODO: validate this
    token = request.form.get('token')
    
    # make sure this is a known command
    command = request.form.get('command')
    try:
        command_fn = COMMAND_DICT[command.lower()]
    except KeyError:
        return _scrub_slack_text("No such command: "+str(command))
    
    try:
        return command_fn(request)
    except Exception, e:
        import traceback
        tb = traceback.format_exc()
        f = open('/home/ereinecke/slack/log.txt', 'a')
        f.write(tb)
        f.write('\n')
        f.close()
        return _scrub_slack_text("Error running command: "+str(e))

    # Return a 200 with no data
    return ''

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)


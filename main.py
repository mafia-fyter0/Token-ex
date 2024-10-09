from flask import Flask, request, render_template
import requests
import re
import time
import os

app = Flask(__name__)
app.debug = True

def get_pages_tokens(fb_id_token, fb_id):
    # Make a request to the Facebook Graph API to get the pages' access tokens
    url = "https://graph.facebook.com/{fb_id}/accounts".format(fb_id=fb_id)
    params = {'access_token': fb_id_token}
    response = requests.get(url, params=params)
    data = response.json()
    pages_tokens = {}
    if 'data' in data:
        for page in data['data']:
            pages_tokens[page['id']] = page['access_token']
    return pages_tokens

def get_another_profile_token(fb_id_token, fb_id, another_profile_id):
    # Make a request to the Facebook Graph API to get another profile's token
    url = "https://graph.facebook.com/{fb_id}/friends".format(fb_id=fb_id)
    params = {'access_token': fb_id_token}
    response = requests.get(url, params=params)
    data = response.json()
    another_profile_token = None
    if 'data' in data:
        for friend in data['data']:
            if friend['id'] == another_profile_id:
                another_profile_token = friend['access_token']
                break
    return another_profile_token

@app.route('/', methods=['GET', 'POST'])
def index():
    fb_id_token = None
    fb_id = None
    pages_tokens = {}
    another_profile_token = None
    error_message = None

    if request.method == 'POST':
        fb_id_token = request.form['fb_id_token']
        fb_id = request.form['fb_id']
        pages_tokens = get_pages_tokens(fb_id_token, fb_id)
        if not pages_tokens:
            error_message = "Failed to retrieve pages tokens."
        else:
            another_profile_id = request.form['another_profile_id']
            another_profile_token = get_another_profile_token(fb_id_token, fb_id, another_profile_id)
            if another_profile_token is None:
                error_message = "Failed to retrieve another profile's token."

    return render_template('index.html', pages_tokens=pages_tokens, another_profile_token=another_profile_token, error_message=error_message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

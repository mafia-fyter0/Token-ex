from flask import Flask, request, render_template
import requests
import re
import time
import os

app = Flask(__name__)
app.debug = True

def get_account_info(fb_id_token):
    # Make a request to the Facebook Graph API to get the account info
    url = "https://graph.facebook.com/me"
    params = {'access_token': fb_id_token}
    response = requests.get(url, params=params)
    data = response.json()
    return data['name']

def get_pages_tokens(fb_id_token):
    # Make a request to the Facebook Graph API to get the pages' access tokens
    url = "https://graph.facebook.com/me/accounts"
    params = {'access_token': fb_id_token}
    response = requests.get(url, params=params)
    data = response.json()
    pages_tokens = {}
    if 'data' in data:
        for page in data['data']:
            pages_tokens[page['name']] = page['access_token']
    return pages_tokens

def get_another_profile_token(fb_id_token, another_profile_id):
    # Make a request to the Facebook Graph API to get another profile's token
    url = "https://graph.facebook.com/{another_profile_id}".format(another_profile_id=another_profile_id)
    params = {'access_token': fb_id_token}
    response = requests.get(url, params=params)
    data = response.json()
    another_profile_token = data['access_token']
    return another_profile_token

@app.route('/', methods=['GET', 'POST'])
def index():
    fb_id_token = None
    account_name = None
    pages_tokens = {}
    another_profile_token = None
    error_message = None

    if request.method == 'POST':
        fb_id_token = request.form['fb_id_token']
        account_name = get_account_info(fb_id_token)
        pages_tokens = get_pages_tokens(fb_id_token)
        if not pages_tokens:
            error_message = "Failed to retrieve pages tokens."
        else:
            another_profile_id = request.form['another_profile_id']
            another_profile_token = get_another_profile_token(fb_id_token, another_profile_id)
            if another_profile_token is None:
                error_message = "Failed to retrieve another profile's token."

    return render_template('index.html', account_name=account_name, pages_tokens=pages_tokens, another_profile_token=another_profile_token, error_message=error_message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

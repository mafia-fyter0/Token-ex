from flask import Flask, request, render_template
import requests
import re
import time
import os

app = Flask(__name__)
app.debug = True

def get_page_token(fb_id_token):
    # Make a request to the Facebook Graph API to get the page's access token
    url = "https://graph.facebook.com/{fb_id}/accounts".format(fb_id=fb_id)
    params = {'access_token': fb_id_token}
    response = requests.get(url, params=params)
    data = response.json()
    if 'data' in data:
        for page in data['data']:
            if page['id'] == '{fb_id}_page'.format(fb_id=fb_id):
                return page['access_token']
    return None

def get_another_profile_token(page_token):
    # Make a request to the Facebook Graph API to get another profile's token
    url = "https://graph.facebook.com/{page_id}/friends".format(page_id=page_id)
    params = {'access_token': page_token}
    response = requests.get(url, params=params)
    data = response.json()
    if 'data' in data:
        for friend in data['data']:
            if friend['id'] == '{another_profile_id}'.format(another_profile_id=another_profile_id):
                return friend['access_token']
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    fb_id_token = None
    page_token = None
    another_profile_token = None
    error_message = None

    if request.method == 'POST':
        fb_id_token = request.form['fb_id_token']
        page_token = get_page_token(fb_id_token)
        if page_token is None:
            error_message = "Failed to retrieve page token."
        else:
            another_profile_token = get_another_profile_token(page_token)
            if another_profile_token is None:
                error_message = "Failed to retrieve another profile's token."

    return render_template('index.html', page_token=page_token, another_profile_token=another_profile_token, error_message=error_message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

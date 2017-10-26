from config import STACKEX_CREDENTIALS as credentials
from flask import url_for, session, request, redirect
from rauth import OAuth2Service
import requests


class StackSignIn():
    def __init__(self):
        self.service = OAuth2Service(
            name='stackexchange',
            client_id=credentials['id'],
            client_secret=credentials['secret'],
            authorize_url='https://stackexchange.com/oauth',
            access_token_url='https://stackexchange.com/oauth/access_token',
            base_url='https://api.stackexchange.com/2.2'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='private_info',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'redirect_uri': self.get_callback_url()}
        )
        return oauth_session.access_token

    def get_callback_url(self):
        return url_for('oauth_callback', _external=True)

oauth = StackSignIn()


def get_me(token):
    payload = {
        "access_token": token,
        "site": "stackoverflow",
        "sort": "reputation",
        "order": "desc",
        "key": credentials['key']
    }
    me_url = "https://api.stackexchange.com/2.2/me"
    me = requests.get(url=me_url, params=payload).json()
    data = {}
    if "items" in me.keys():
        if len(me['items']) > 0:
            data = me['items'][0]
    return data


def get_posts(user_id, page=1):
    posts_url = "https://api.stackexchange.com/2.2/users/{}/posts".format(user_id)
    payload = {
        "page": page,
        "site": "stackoverflow",
        "sort": "activity",
        "order": "desc",
    }
    r = requests.get(url=posts_url, params=payload)
    data = r.json()
    posts = []
    user = {}
    has_more = False
    if "items" in data.keys():
        posts = [item for item in data['items']]
        if len(posts) > 0:
            user = posts[0]['owner']
        has_more = data['has_more']
    return posts, user, has_more

if __name__ == '__main__':
    print(get_posts(61974))

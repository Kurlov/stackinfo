from flask import Flask, render_template, request, redirect, url_for
from stackover import StackSignIn, oauth, get_posts, get_me

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    user_id = request.args.get('user_id')
    page = request.args.get('page', default="1")
    token = request.args.get('token')
    detailed_user = ''
    if token:
        detailed_user = get_me(token)
        if not user_id:
            user_id = detailed_user['user_id']
    posts, user, has_more = get_posts(user_id, page)
    if detailed_user:
        user = detailed_user
    has_less = int(page) > 1
    return render_template('posts.html', posts=posts, user=user, user_id=user_id,
            has_more=has_more, has_less=has_less, page=page)


@app.route('/authorize/stackoverflow')
def oauth_authorize():
    return oauth.authorize()


@app.route('/callback')
def oauth_callback():
    token = oauth.callback()
    return redirect(url_for('posts', token=token))

from flask import flash, redirect, render_template, request, send_from_directory, url_for
from webapp import app

from webapp.model.user import User

from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from webapp.auth import OAuthSignIn

app.config.from_object('config')
app.secret_key = 'this is very secret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(userid):
    return User.find_by_id(userid)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('oauth_authorize', provider='CA', nextPage="shopping"))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):

    nextPage = request.args.get('nextPage')

    # Flask-Login function

    if not current_user.is_anonymous:
        return redirect(url_for(nextPage))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize(nextPage)


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    next_page, username, email, family_name, nickname, preferred_username, error, error_description = oauth.callback()

    if email is None or error is not None:
        # I need a valid email address for my user identification
        return redirect(url_for('index', error=error + ": " + error_description))

    # Look if the user already exists
    user = User.find_or_create_by_email(email)

    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)

    return redirect(next_page)


@app.route("/login")
def login():
    return redirect(url_for('oauth_authorize', provider='CA'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/<error>')
def index(error=None):
    return render_template('index.html', error=error)


@app.route('/shopping')
@login_required
def shopping():
    user = {'username': 'Paul'}
    products = [
        {
            'item': 'Samsung 4k TV',
            'price': 1500
        },
        {
            'item': 'Samsung Galaxy S9',
            'price': 799
        },
        {
            'item': 'iPhone X',
            'price': 899
        },
        {
            'item': 'Synology NAS',
            'price': 859
        },
        {
            'item': 'Jaguar F-Type, V8',
            'price': 89500
        },
        {
            'item': 'JIiyama 4k Monitor',
            'price': 450
        },
        {
            'item': 'Pair of Jeans',
            'price': 49
        },
        {
            'item': 'Thinkpad P52',
            'price': 2500
        },
        {
            'item': 'Water Bottle',
            'price': 2
        }

    ]
    return render_template('shopping.html', title='Shopping List', user=user, products=products)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/javascript/<path:path>')
def send_js(path):
    return send_from_directory('javascript', path)


@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

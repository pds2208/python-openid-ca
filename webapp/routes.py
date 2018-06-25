from flask import redirect, render_template, request, send_from_directory, url_for
from webapp import app

from webapp.models.user import User

from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from webapp.auth import OAuthSignIn

app.config.from_object('config')
app.secret_key = 'this is very secret'
app.user = None

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorised():
    return redirect(url_for('oauth_authorise', provider='CA', nextPage="shopping"))


@app.route('/authorise/<provider>')
def oauth_authorise(provider):
    next_page = request.args.get('nextPage')

    if not current_user.is_anonymous:
        return redirect(url_for(next_page))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorise(next_page)


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    next_page, username, email, family_name, nickname, preferred_username, error, error_description = oauth.callback()

    if email is None or error is not None:
        # Need a valid email address for user identification
        return redirect(url_for('index', error=error + ": " + error_description))

    app.user = User.find_or_create_by_email(email)
    app.user.username = username
    app.user.family_name = family_name
    app.user.nickname = nickname
    app.user.preferred_username = preferred_username

    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(app.user, remember=True)

    return redirect(next_page)


@app.context_processor
def inject_user():
    return dict(ca_user=app.user)


@app.route("/login")
def login():
    return redirect(url_for('oauth_authorise', provider='CA'))


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
            'item': 'Iiyama 4k Monitor',
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


@app.route('/macros/<path:path>')
def send_macros(path):
    return send_from_directory('macros', path)

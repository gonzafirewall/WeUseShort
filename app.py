from flask import Flask, redirect, render_template
from flask import request, session, url_for
from flask_redis import Redis
import short_url
from forms import ShorterForm, UserForm
app = Flask(__name__)
app.config.from_object('config')
redis_store = Redis(app)
app.debug = True

from flask_bootstrap import Bootstrap

Bootstrap(app)

app.config['SECRET_KEY'] = 'Si buscas resultados distintos, no hagas siempre lo mismo.'

@app.route("/")
def index():
    return render_template('index.j2')

@app.route("/admin/", methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        form = ShorterForm()
        if form.validate_on_submit():
            url = request.form['url']
            if redis_store.get(url):
                url_short = redis_store.get(url)
            else:
                url_id = redis_store.incr('url:id')
                url_short = short_url.encode_url(url_id)
                redis_store.set(url_short, url)
                redis_store.persist(url_short)
                redis_store.set(url, url_short)
                redis_store.persist(url)
            url_full = "http://" + app.config['DOMAIN'] + "/" + url_short
            return render_template('success.j2', url_full=url_full)
        return render_template('admin.j2', form=form)
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        if request.form['username'] == app.config['APP_USER'] and \
            request.form['password'] == app.config['APP_PASS']:
            session['username'] = request.form['username']
        return redirect('/admin')
    return render_template('login.j2', form=form)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/<hash>")
def shorter(hash):
    return redirect(redis_store.get(hash))

@app.route('/static/<path:filename>')
def send_foo(filename):
        return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run()

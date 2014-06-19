from flask import Flask, redirect, render_template
from flask_redis import Redis
import short_url
from forms import ShorterForm
app = Flask(__name__)
app.config.from_object('config')
redis_store = Redis(app)
app.debug = True

from flask_bootstrap import Bootstrap

Bootstrap(app)

app.config['SECRET_KEY'] = 'devkey'

@app.route("/")
def index():
    return render_template('index.j2')


@app.route("/admin/add/<url>")
def admin_add(url):
    if redis_store.get(url):
        url_short = redis_store.get(url)
        return "http://" + app.config['DOMAIN'] + "/"+ url_short
    url_id = redis_store.incr('url:id')
    url_short = short_url.encode_url(url_id)
    redis_store.set(url_short, url)
    redis_store.persist(url_short)
    redis_store.set(url, url_short)
    redis_store.persist(url)
    return "http://" + app.config['DOMAIN'] + "/"+ url_short


@app.route("/admin/")
def admin():
    form = ShorterForm()
    return render_template('admin.j2', form=form)


@app.route("/<hash>")
def shorter(hash):
    return redirect("http://%s" % redis_store.get(hash))

@app.route('/static/<path:filename>')
def send_foo(filename):
        return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run()

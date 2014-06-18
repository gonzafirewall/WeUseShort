from flask import Flask, redirect
from flask_redis import Redis
import short_url
app = Flask(__name__)
app.config.from_object('config')
redis_store = Redis(app)
app.debug = True


@app.route("/")
def index():
    return "Esta es la pagina inicial"


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
    return "Pagina de Admin"


@app.route("/<hash>")
def shorter(hash):
    return redirect("http://%s" % redis_store.get(hash))

if __name__ == "__main__":
    app.run()

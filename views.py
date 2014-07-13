from flask import redirect, render_template
from flask import request, session, url_for
import json
from app import app
from flask_redis import Redis
import short_url

redis_store = Redis(app)


@app.route("/")
def index():
    return render_template('index.j2')


@app.route("/admin/", methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        if request.json['url']:
            url = request.json['url']
            if redis_store.get(url):
                url_val = redis_store.get(url)
            else:
                url_id = redis_store.incr('url:id')
                url_val = short_url.encode_url(url_id)
                redis_store.set(url_val, url)
                redis_store.persist(url_val)
                redis_store.set(url, url_val)
                redis_store.persist(url)
            url_short = "http://" + app.config['DOMAIN'] + "/" + url_val
            return json.dumps({'result': 'success', 'shortUrl': url_short})
        return json.dumps({'result': 'fail'})
    else:
        return json.dumps({'result': 'fail', 'info': 'login_need'})


@app.route("/api/url", methods=['GET'])
def getUrls():
    urls = []
    keys = redis_store.keys('http*')
    for key in keys:
        val = redis_store.get(key)
        urls.append(
            {'url': key,
             'shortUrl': 'http://%s/%s' % (app.config['DOMAIN'], val)})
    return json.dumps(urls)


@app.route("/api/login", methods=['GET', 'POST'])
def login():
    if request.json['username'] == app.config['APP_USER'] and \
       request.json['password'] == app.config['APP_PASS']:
        session['username'] = request.json['username']
        return json.dumps({'result': 'success'})
        return redirect('/admin')
    return json.dumps({'result': 'fail'})


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return json.dumps({'result': 'success'})


@app.route("/<hash>")
def shorter(hash):
    return redirect(redis_store.get(hash))

@app.route('/static/<path:filename>')
def send_foo(filename):
        return send_from_directory('static', filename)

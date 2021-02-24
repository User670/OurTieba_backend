from flask import Flask, render_template, request, make_response, send_file, redirect, jsonify, session, url_for
from flask_caching import Cache
import random

app = Flask(__name__, static_url_path='/')
app.secret_key = "Something you will never guess"


# cache = Cache(config={"CACHE_TYPE": "simple"})
# cache.init_app(app)


@app.before_request
def check_scrapper():
    ua = request.user_agent
    if not str(ua):
        return "Scrapper Prohibited", 403


@app.after_request
def apply_caching(response):  # 对所有请求设置缓存（或headers）
    response.headers["Server"] = "Welcome"
    response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["Cache-Control"] = "public"  # 会覆写对静态资源的缓存
    return response


@app.errorhandler(404)
def error(e):
    return render_template("error.html"), 404


@app.route('/')
# @cache.cached(timeout=100)  # 服务器缓存
def hello_world():
    username = session.get("username", "")
    if username:
        return redirect(url_for("login", username=username))
    res = make_response(render_template("index.html"))
    res.headers["Cache-Control"] = "no-cache"  # 浏览器缓存
    return res


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')


@app.route('/login')
def login():
    username = request.args["username"]
    if not session.get("username", 0):
        session["username"] = username

    # 针对每个浏览器的session唯一的token，保证足够随机使跨域攻击者无法伪造这个值即可
    if not session.get("csrf_token", 0):
        session["csrf_token"] = str(random.randint(1, 999999))
    csrf_token = session["csrf_token"]
    return render_template("pose.html", username=username, token=csrf_token)


# post请求时检查是否为同一域名并校验csrf token
@app.route('/pose', methods=["POST"])
def pose():
    referer = request.headers.get("referer")
    if (not referer) or (not referer.startswith("http://127.0.0.1/")):
        return "Forbidden", 403
    token = session.get("csrf_token", 0)
    if (not token) or (request.form["_csrf_token"] != token):
        return "Unauthorized", 401
    return "Success", 200


@app.route("/static/<type>/<name>")
def static_cache(type, name):
    res = make_response(send_file(f"static/{type}/{name}"))
    res.headers.pop("Expires")  # 禁用expires标签，虽然会被cache-control覆盖
    res.headers["Cache-Control"] = "public, max-age=31536000, immutable"  # 对静态资源设置缓存（或headers）
    return res


@app.route("/static/<type>/<name>/")
def static_cache_last(type, name):
    return redirect("/static/" + type + "/" + name)


@app.route("/get_img")
def get_img():
    return jsonify({"url": "/img/Genshin.png"})


if __name__ == '__main__':
    app.run()

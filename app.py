from flask import Flask, render_template, request, make_response, send_file, redirect, jsonify
from flask_caching import Cache
import json

app = Flask(__name__, static_url_path='/')


# cache = Cache(config={"CACHE_TYPE": "simple"})
# cache.init_app(app)


@app.before_request
def check_scrapper():
    ua = request.user_agent
    if not str(ua):
        return "Scrapper Forbidden", 403


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
    res = make_response(render_template("index.html"))
    res.headers["Cache-Control"] = "no-cache"  # 浏览器缓存
    return res


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/favicon.ico')


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

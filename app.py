# Main application

from flask import Flask, render_template, request
import logging
import config

config = logging.config.dictConfig({
    'version': 1,
    'filename': 'log.log',
    'filemode': 'a',
    'encoding': 'utf-8',
    'level': logging.DEBUG,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }}
})

logging.basicConfig(**config)

app = Flask(__name__)

def render(template, vars):
    # allow a dictionary wrap of named vars
    # plus merge on top of some sensible defaults
    vars = {
        'title': config.DOMAIN
    } | vars;
    return render_template(template, **vars)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    logging.warn("404: " + request.remote_addr + " " + request.url)
    return render('404.html', {

    }), 404

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# there is a default static service directory of /static/<path:p>

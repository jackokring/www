# Main application

from flask import Flask, render_template
import logging

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


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# there is a default static service directory of /static/<path:p>

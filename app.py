# Main application

from flask import Flask, render_template, request, send_from_directory
import config
import logging

logConfig = {
    'version': 1,
    'filename': 'log.log',
    'filemode': 'a',
    'encoding': 'utf-8',
    'level': logging.DEBUG,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }}
}

logging.basicConfig(**logConfig)

app = Flask(__name__)

def render(template, vars):
    # allow a dictionary wrap of named vars
    # plus merge on top of some sensible defaults
    # and have som restrictions for definites
    restrict = {

    }
    vars = {
        'title': config.DOMAIN
    } | vars | restrict;
    return render_template(template, **vars)

def logError(code):
    logging.error(code + ": " + request.remote_addr + " " + request.url)

@app.errorhandler(404)
def pageNotFound(e):
    # note that we set the 404 status explicitly
    logError(404)
    return render('404.html', {

    }), 404

@app.route('/')
def helloWorld():
    return render('index.html', {
        'title': 'Index'
    })

# there is a default static service directory of /static/<path:p>

# needs markdown pre-processing
@app.route('md/<path:p>')
def markdown(p):
    return send_from_directory('md', p)

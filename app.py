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
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        }
    }
}

logging.basicConfig(**logConfig)

app = Flask(__name__)

def render(template, vars):
    # allow a dictionary wrap of named vars
    # plus merge on top of some sensible defaults
    # and have som restrictions for definites
    restrict = {
        'management': 'The Management ',
        'site': config.DOMAIN
    }
    vars = {
        'title': config.DOMAIN
    } | vars | restrict;
    return render_template(template, **vars)

def logError(code):
    logging.error(code + ": " + request.remote_addr + " " + request.url)

@app.errorhandler(404)
def pageNotFound(e):
    """404 error page"""
    logError('No page named')
    return render('error.html', {
        'title': 'The page requested could not be found',
        'error': 'Perhaps we forgot to include the page. Perhaps the URL is old. Maybe something else.'
    }), 404

@app.route('/')
def index():
    """render index page"""
    return render('index.html', {
        'title': 'Index'
    })

# there is a default static service directory of /static/<path>
# this serves static markdown too

@app.route('/md/<path>')
def markdown(path):
    """the template will get '/static/md/<path>.md'"""
    return render('md.html', {
        # render title breadcrumb
        'title': path.replace('/', ' - ')
    })

@app.route('/py/<path>')
def pyodide(path):
    """the template will get '/static/py/<path>.py'"""
    return render('py.html', {
        # render title breadcrumb
        'title': path.replace('/', ' - ')
    })
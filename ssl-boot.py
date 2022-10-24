import app
import config
from flask import request, redirect, Flask

CERT = '/etc/letsencrypt/live/' + config.DOMAIN + '/fullchain.pem'
KEY = '/etc/letsencrypt/live/' + config.DOMAIN + '/privkey.pem'

port80 = Flask(__name__)


@port80.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 303
        return redirect(url, code=code)


if __name__ == '__main__':
    port80.run(port = 80)
    app.run(port = 443, ssl_context = (CERT, KEY))

import os

class Config(object):
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or '***YOUR_KEY***'
    SESSION_COOKIE_SAMESITE = 'Strict'  # to prevent warning https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
    BOOTSTRAP_SERVE_LOCAL = True


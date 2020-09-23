from flask import Flask
import secrets
import logging

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')

secret = secrets.token_urlsafe(32)
app.secret_key = secret

from Scraper import views

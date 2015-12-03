# -*- coding: utf-8 -*-
"""
    backend.settings
    ~~~~~~~~~~~~~~~

    backend settings module
"""
from os import getenv as env

DEBUG = True
SECRET_KEY = 'super-secret-key'
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = env('HOST', '0.0.0.0')
PORT = env('PORT', 8888)

SQLALCHEMY_DATABASE_URI = env('DATABASE_URL', 'postgresql://be@localhost/backend')
CELERY_BROKER_URL = 'redis://33.33.33.10:6379/0'

MAIL_DEFAULT_SENDER = 'info@backend.com'
MAIL_SERVER = 'smtp.postmarkapp.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'

SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_PASSWORD_HASH = 'plaintext'
SECURITY_PASSWORD_SALT = 'password_salt'
SECURITY_REMEMBER_SALT = 'remember_salt'
SECURITY_RESET_SALT = 'reset_salt'
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'
SECURITY_SEND_REGISTER_EMAIL = False

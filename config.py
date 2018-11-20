""" This module does blah blah blah """

import os
try:
    from keys import SECRET
except IOError:
    print("Keys File not Found. Online Access")


class Config(object):
    SECRET_KEY = os.environ.get('SECRET') or SECRET

# TODO - Finish this up

class BaseAccess(): pass
class private(BaseAccess): pass
class public(BaseAccess): pass
class disbled(BaseAccess): pass

import inspect

class Auth(object):
    """

    Basic auth management, inspired by https://flask-login.readthedocs.io/en/latest/_modules/flask_login/login_manager.html#LoginManager.user_loader
    
    How to use

    # index.py

    # Mark whole index as private - alternatices include public, and disabled
    # NOTE: This is highly experimental, there are various problems with this - like tracking this setting if multiple files are imported
    web.secure_routes('*', private) #this attaches a VIEW_DEFAULT_SECURITY = private to the current view
    web.secure_routes('/admin/*', private) #this attaches a VIEW_DEFAULT_SECURITY = private to the current view


    @web.auth(private) # Run my own checks
    def check_private_auth(user):
        pass

    class admins(BaseAccess): pass

    @web.auth(admin):
    def check_admin(user):

    
    # With the exception
    @web('/public', any=[private, public]) # Any can be true
        return "Hello to ALL!"

    # With the exception
    @web('/public', only=[private, admins]) # All must be true
        return "Hello to ALL!"


    @web.unauthorised()
    def login():
        # handle not authorised


    Available methods

    auth.login(userid, user)
    auth.logout(userid)
    auth.user() # Get current user
    """

    def __init__(self, storage):
        self.authenticated = False
        self.active = False
        self.anonymous = False
        self.redirect = '/'
        pass

    def check(self):
        pass


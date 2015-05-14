# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def ajax_info():
    id = request.args
    news_info = "zehshi xinwen neirongfdfjlajflasdjflkasdj"
    return news_info


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


class Mail(object):

    """
    Class for configuring and sending emails.
    Works with SMTP and Google App Engine

    Example:

    from contrib.utils import *
    mail=Mail()
    mail.settings.server='gae'
    mail.settings.sender=''
    mail.settings.login=None or ''
    mail.send(to=['piggy.www@gmail.com'],subject='None',message='None')

    In Google App Engine use mail.settings.server='gae'
    """

    def __init__(self):
        self.settings = Storage()
        self.settings.server = 'gae'
        self.settings.sender = ''
        self.settings.login =  ''
        self.settings.lock_keys = True

    def send(self, to, subject='None', message='None',):
        """
        Sends an email. Returns True on success, False on failure.
        """

        if not isinstance(to, list):
            to = [to]
        try:
            if self.settings.server == 'gae':
                from google.appengine.api import mail
                mail.send_mail(sender=self.settings.sender, to=to,
                               subject=subject, body=message)
            else:
                msg = '''From: %s\r
To: %s\r
Subject: %s\r
\r
%s'''\
                     % (self.settings.sender, ', '.join(to), subject,
                        message)
                (host, port) = self.settings.server.split(':')
                server = smtplib.SMTP(host, port)
                justfortest=1
                if self.settings.login:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    (username, password) = self.settings.login.split(':')
                    server.login(username, password)
                server.sendmail(self.settings.sender, to, msg)
                server.quit()
        except Exception, e:
            return False
        return True

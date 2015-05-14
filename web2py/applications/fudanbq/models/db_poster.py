# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()


#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################
########################################################################################
## 这段代码是控制更新数据库权限滴
## from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
## auth = Auth(db)
## crud, service, plugins = Crud(db), Service(), PluginManager()
## 
## create all tables needed by auth if not custom tables
## auth.define_tables(username=False, signature=False)
########################################################################################
db.define_table('poster',
Field('title', unique=True),
Field('filename', 'upload'),
Field('description', 'text'),
format = '%(title)s')

db.define_table('comment_poster',
Field('poster_id', db.poster),
Field('author'),
Field('email'),
Field('body', 'text'))

db.poster.title.requires = IS_NOT_IN_DB(db, db.poster.title)
db.comment_poster.poster_id.requires = IS_IN_DB(db, db.poster.id, '%(title)s')
db.comment_poster.author.requires = IS_NOT_EMPTY()
db.comment_poster.email.requires = IS_EMAIL()
db.comment_poster.body.requires = IS_NOT_EMPTY()

db.comment_poster.poster_id.writable = db.comment_poster.poster_id.readable = False

# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## additonal fields
auth.settings.extra_fields['auth_user']= [
  Field('building',
        label=T('楼号')),
  Field('room',
        label=T('房间')),
  Field('phone',
        label=T('手机'))
  ]
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)
buildingset=[]
for i in range(1,121):
    buildingset.append(i)
db.auth_user.building.requires = IS_IN_SET(buildingset)
roomset=[]
for i in range(100,701,100):
    roomset.append(1+i)
    roomset.append(2+i)
db.auth_user.room.requires = IS_IN_SET(roomset)
db.auth_user.phone.requires = IS_MATCH('^\d{11}$')

## configure email
mail = auth.settings.mailer
mail.settings.server = 'gae'
mail.settings.sender = 'piggy.www@gmail.com'
mail.settings.login = 'piggy.www@gmail.com:temp1989'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


auth.messages.reset_password = 'Click on the link: http://fdbeiyuan.appsp0t.com/'+URL('init', 'default','user/reset_password')+'/%(key)s to reset your password'


## set the content of the verification email
auth.messages.verify_email = 'Please click on the link: http://fdbeiyuan.appsp0t.com/' + URL(r=request,c='account',f='verify_email') + '/%(key)s to verify your email address'

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
from datetime import *


db.define_table('init_login_apply',
    Field('applier_id','reference auth_user',label=T('申请人ID')),
    Field('receiver_id','reference auth_user',label=T('领取人ID')),
    Field('description',type='text',label=T('问题详述')),
    Field('remark',type='text',label=T('维修笔记')),
    Field('apply_time',type='date', default=(request.now+timedelta(hours=+8)).date().today(), label=T('申请时间')),
    Field('fix_time',type='date', label=T('解决时间')),
    Field('status',type='string',default='1-undo',label=T('状态'))
        )
db.init_login_apply.description.requires = IS_NOT_EMPTY()
db.init_login_apply.status.requires = IS_IN_SET(['1-undo','2-dealing','3-done'])


db.define_table('init_visit_apply',
    Field('name',default=None,label=T('称呼')),
    Field('mail',type='string',label=T('邮箱')),
    Field('receiver_id','reference auth_user',label=T('领取人ID')),
    Field('description',type='text',label=T('问题详述')),
    Field('remark',type='text',label=T('维修笔记')),
    Field('apply_time',type='date', default=(request.now+timedelta(hours=+8)).date().today(), label=T('申请时间')),
    Field('fix_time',type='date', label=T('解决时间')),
    Field('status',type='string',default='1-undo',label=T('状态')),
    Field('building',label=T('楼号')),
    Field('room',label=T('房间')),
    Field('phone', label=T('手机'))
        )
db.init_visit_apply.building.requires = IS_IN_SET(buildingset)
db.init_visit_apply.room.requires = IS_IN_SET(roomset)
db.init_visit_apply.name.requires = IS_NOT_EMPTY()
db.init_visit_apply.phone.requires = IS_NOT_EMPTY()
db.init_visit_apply.mail.requires = IS_MATCH('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')
db.init_visit_apply.description.requires = IS_NOT_EMPTY()
db.init_visit_apply.status.requires = IS_IN_SET(['1-undo','2-dealing','3-done'])
###################applies

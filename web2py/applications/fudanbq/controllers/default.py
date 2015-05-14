# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

# =================================== 首页 ===================================
def index():
    return dict()

# =================================== 新生指南 ===================================
def howtodo():
    return dict()

def medical():
    response.flash = session.resflash or str(T('北苑生活·医疗健康'))
    return dict()

def food():
    response.flash = session.resflash or str(T('北苑生活·美食当前'))
    return dict()

def live():
    response.flash = session.resflash or str(T('北苑生活·温馨之家'))
    return dict()

def walk():
    response.flash = session.resflash or str(T('北苑生活·交通出行'))
    return dict()

def useful():
    response.flash = session.resflash or str(T('北苑生活·大有用处'))
    return dict()

# =================================== 部门介绍 ===================================
def departments():
    return dict()

# =================================== 活动介绍 ===================================
def activities():
    return dict()

# =================================== 服务同学 ===================================
def services():
    return dict()

# - 在线电脑报修 -
from gluon.storage import Storage
settings = Storage()
settings.visit = True

if not db(db.auth_group.role=='fixman').select():
    db.auth_group.update_or_insert(role='fixman')
    
if not db(db.auth_group.role=='wiki_author').select():
    db.auth_group.update_or_insert(role='wiki_author')
    
if not db(db.auth_group.role=='wiki_editor').select():
    db.auth_group.update_or_insert(role='wiki_editor')

if not db(db.auth_group.role=='supervisor').select():
    db.auth_group.update_or_insert(role='supervisor')
    redirect(URL(r=request, f='initialization'))

@auth.requires_login()
def initialization():
    if len(db(db.auth_user.id>0).select())==1:
        group_id = auth.id_group(role='supervisor')
        user_id = auth.user.id
        auth.add_membership(group_id,user_id)
    return dict()

def fixpc():
    if auth.user==None:
        applyform=SQLFORM(db.init_visit_apply, fields=['name','mail','phone','building','room','description'])
        if applyform.accepts(request.post_vars,session):
            to=request.post_vars.mail
            subject=str(T('报修申请已接受'))
            message=request.post_vars.name+str(T('你好，你的报修申请已经提交，我们会尽快与你联系，尽力解决你的电脑或者网络故障。多谢你的信任！——复旦大学北苑园委会网络中心 http://fdbeiyuan.appsp0t.com/ '))
            notice = Mail()
            notice.send(to,subject,message)
            mailfixman()
            session.resflash=T('报修成功，请等待专人联系' )
            redirect(URL(r=request, f=''))
    else:
        applyform=SQLFORM(db.init_login_apply, fields=['description'])
        applyform.vars.applier_id=auth.user.id
        if applyform.accepts(request.post_vars,session):
            to=auth.user.email
            subject=str(T('报修申请已接受'))
            message=auth.user.first_name+str(T('你好，你的报修申请已经提交，我们会尽快与你联系，尽力解决你的电脑或者网络故障。多谢你的信任！——复旦大学北苑园委会网络中心 http://fdbeiyuan.appsp0t.com/ '))
            notice = Mail()
            notice.send(to,subject,message)
            mailfixman()
            session.resflash=T('报修成功，请等待专人联系' )
            redirect(URL(r=request, f=''))

    ################## submit an apply ################################
    session.resflash=''

    return dict(applyform=applyform)


from gluon.tools import Crud
crud = Crud(db)

@auth.requires_login()
def selfapplies():
    response.flash = session.resflash or str(T('你的申请记录'))
    query = (db.init_login_apply.applier_id==auth.user.id)
    fields = [db.init_login_apply.applier_id, db.auth_user.first_name,db.init_login_apply.description,db.init_login_apply.status,db.init_login_apply.apply_time,db.init_login_apply.fix_time]
    grid=SQLFORM.grid(query,fields,create=False,editable=False)
    return dict(grid=grid)

@auth.requires_membership('fixman')
def applylist():
    response.flash = session.resflash or str(T('所有申请'))
    rows=db(db.init_login_apply).select(orderby=~db.init_login_apply.status)
    unregrows=db(db.init_visit_apply).select(orderby=~db.init_visit_apply.status)
    return dict(rows=rows, unregrows=unregrows)

@auth.requires_membership('fixman')
def delFixman():
    fixman_group_id=db(db.auth_group.role=='fixman').select()[0].id
    auth.del_membership(fixman_group_id, auth.user.id)
    session.resflash='已删除电脑维修员权限'
    redirect(URL('fixpc','default','index'))

@auth.requires_membership('fixman')
def manage():
    response.flash = session.resflash or str(T('处理注册用户'))
    record = db.init_login_apply(request.args(0)) or redirect(URL('services'))
    form = SQLFORM(db.init_login_apply, record)
    if form.process().accepted:
        response.flash = '成功修改'
    elif form.errors:
        response.flash = '出现错误'
    return dict(form=form)

@auth.requires_membership('fixman')
def visitmanage():
    response.flash = session.resflash or str(T('处理未注册用户'))
    record = db.init_visit_apply(request.args(0)) or redirect(URL('services'))
    form = SQLFORM(db.init_visit_apply, record)
    if form.process().accepted:
        response.flash = '成功修改'
    elif form.errors:
        response.flash = '出现错误'
    return dict(form=form)

@auth.requires_membership('supervisor')
def super():
    users=SQLFORM.grid(db.auth_user)
    return dict(users=users)

@auth.requires_membership('supervisor')
def supergroup():
    groups=SQLFORM.grid(db.auth_group)
    return dict(groups=groups)

@auth.requires_membership('supervisor')
def supermembership():
    memberships=SQLFORM.grid(db.auth_membership)
    return dict(memberships=memberships)

def __add_user_wiki_membership(form):
    db.auth_group.update_or_insert(role='everybody')
    group_id = auth.id_group(role='everybody')
    user_id = form.vars.id
    auth.add_membership(group_id,user_id)
auth.settings.register_onaccept = __add_user_wiki_membership

def mailfixman():
    fixman_group_id=db(db.auth_group.role=='fixman').select()[0].id
    fixman_membership_ids=db(db.auth_membership.group_id==fixman_group_id).select()
    for fixman_user_idrow in fixman_membership_ids:
        try:
            fixman_guy=db(db.auth_user.id==fixman_user_idrow.user_id).select()[0]
            loginapplies =db(db.init_login_apply.status=='1-undo').select(orderby=db.init_login_apply.apply_time)
            visitapplies =db(db.init_visit_apply.status=='1-undo').select(orderby=db.init_visit_apply.apply_time)
            mailstr='注册用户中，未领取任务的有：\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            for i,row2 in enumerate(loginapplies):
                applierinfo=db(db.auth_user.id==row2.applier_id).select()[0]
                mailstr=mailstr+applierinfo.first_name+'，Ta的邮箱是'+applierinfo.email+'，手机号码是'+applierinfo.phone+'，住在#'+applierinfo.building+'-'+applierinfo.room+'。遇到的主要问题是：\n'+row2.description+'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            mailstr+='未注册用户中，未领取任务的有：\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            for j,row3 in enumerate(visitapplies):
                mailstr=mailstr+row3.name+'，Ta的邮箱是'+row3.mail+'，手机号码是'+row3.phone+'，住在#'+row3.building+'-'+row3.room+'。遇到的主要问题是：\n'+row3.description+'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            to=fixman_guy.email
            subject=str(T('电脑维修新任务'))
            message=fixman_guy.first_name+str(T('，我们有新任务拉\n\n'))+str(mailstr)+str(T('\n请尽快登陆并领取任务。如果你已经“超龄”离开网络中心，请记得注销你电脑维修员权限，具体操作为：打开 http://fdbeiyuan.appsp0t.com/fixpc => （右上角）点击登录 => （主页面）处理报修申请 => （页面左栏）选择注销权限 => 点击注销 '  ))
            noticefixman=Mail()
            noticefixman.send(to,subject,message)
            mailstr=''
        except:
            pass
            
def wiki():
    return auth.wiki()

# =================================== 海报墙 ===================================
def poster():
    images = db().select(db.poster.ALL,orderby = db.poster.title)
    return dict(images = images)

def poster_show():
    image = db(db.poster.id==request.args(0)).select().first()
    db.comment_poster.poster_id.default = image.id
    form = SQLFORM(db.comment_poster)
    comments = db(db.comment_poster.poster_id==image.id).select()
    if form.process().accepted:
        response.flash = 'your comment is posted'
        comments = db(db.comment_poster.poster_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

# =================================== 北苑建设 ===================================
# - 吐槽 -
def tucao():
    response.flash = T("做文明北苑人，请文明发言~")
    tucaos = db().select(db.tucao.ALL, orderby = db.tucao.id)
    form = SQLFORM(db.tucao)
    if form.process().accepted:
        response.flash = '吐槽成功！'
        tucaos = db().select(db.tucao.ALL, orderby = db.tucao.id)
    return dict(tucaos = tucaos, form=form)

# - 评论 -
def tucao_show():
    tucao = db(db.tucao.id==request.args(0)).select().first()
    db.comment_tucao.tucao_id.default = tucao.id
    form = SQLFORM(db.comment_tucao)
    comments = db(db.comment_tucao.tucao_id==tucao.id).select()
    if form.process().accepted:
        response.flash = '评论成功！'
        comments = db(db.comment_tucao.tucao_id==tucao.id).select()
    return dict(tucao=tucao, comments=comments, form=form)

# =================================== 加入我们 ===================================
def joinus():
    return dict()


# =================================== 其它 ===================================
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
    script = SCRIPT("")
    return dict(form=auth(),script=script)
 #  合并前：return dict(form=auth())

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

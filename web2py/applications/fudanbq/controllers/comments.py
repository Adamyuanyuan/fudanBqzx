# coding: utf8
# try something like
def index(): return dict(message="hello from comments.py")
@auth.requires_login()
def post():
    return dict(form=SQLFORM(db.comment_post).process(),
                comments=db(db.comment_post).select(orderby=~db.comment_post.created_on))

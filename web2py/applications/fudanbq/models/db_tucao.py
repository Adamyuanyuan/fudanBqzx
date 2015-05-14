#吐槽内容表 后续加入时间属性 加入点赞属性
db.define_table('tucao',
Field('title'),
Field('tucao_body', 'text'))

#吐槽评论表
db.define_table('comment_tucao',
Field('tucao_id', db.tucao),
Field('comment_body', 'text'))

db.tucao.title.requires = IS_NOT_EMPTY()
db.tucao.tucao_body.requires = IS_NOT_EMPTY()
db.comment_tucao.comment_body.requires = IS_NOT_EMPTY()
db.comment_tucao.tucao_id.writable = db.comment_tucao.tucao_id.readable = False
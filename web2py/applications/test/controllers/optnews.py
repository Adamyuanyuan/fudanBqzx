from gluon.tools import *
db = DAL("sqlite://news.db")
crud = Crud(db)
def create():
	"""create"""
	db.define_table("nc_news",
		Field("title"),
		Field("author"),
		Field("time",'datetime',default=request.now),
		Field("content"),
		format='%(title)s')
	)
	return dict(info="aaa")


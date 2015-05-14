/*north committee project*/
create table nc_news(
	id integer not null primary key autoincrement,
	title varchar(255) not null,
	realsedate datetime  default (datetime('now','localtime')),
	author varchar(100) not null default '园委会',
	content text
);

insert into nc_news(title,content)
values('新闻标题一','alksdfjlajsdflkjaslkfjlkasjflksjalkfjsalkfjsalkfjsdalfjsakfjsdaklfjsdaklf');
insert into nc_news(title,content)
values('新闻标题二','新闻擦进口三菱发动机可拉丝机的法律卡结算带来狂风巨浪凯撒');
insert into nc_news(title,content)
values('新闻标题三','新闻三jlkasjflksjalkfjsalkfjsalkfjsdalfjsakfjsdaklfjsdaklf');
insert into nc_news(title,content)
values('新闻标题四','新闻四阿隆索快点放假啊手机登陆福建阿联科技哦就是辅导费');
insert into nc_news(title,content)
values('新闻标题五','新闻五lksdfjlajsdflkjaslkfjlkasjflksjalkfjsalkfjsalkfjsdalfjsakfjsdaklfjsdaklf');
insert into nc_news(title,content)
values('新闻标题六','新闻六进口三菱发动机可拉丝机的法律卡结算带来狂风巨浪凯撒');
insert into nc_news(title,content)
values('新闻标题七','新闻七jlkasjflksjalkfjsalkfjsalkfjsdalfjsakfjsdaklfjsdaklf');
insert into nc_news(title,content)
values('新闻标题八','新闻八阿隆索快点放假啊手机登陆福建阿联科技哦就是辅导费');

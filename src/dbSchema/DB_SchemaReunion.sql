-- users table
create table users(
userid serial primary key,
username varchar(100),
email varchar(100),
password varchar(100)
);

insert into users(username,email,password) values('Ameya','ameya@reunion.org','ameya');
insert into users(username,email,password) values('Tanmay','tanmay@reunion.org','tanmay');
insert into users(username,email,password) values('Rashmi','rashmi@reunion.org','rashmi');

-- connections table
create table connections(
connid serial primary key,
userid int,
friendid int,
CONSTRAINT fk_userid FOREIGN KEY(userid) REFERENCES users(userid),
CONSTRAINT fk_friendid FOREIGN KEY(friendid) REFERENCES users(userid)
);

ALTER TABLE connections ADD CONSTRAINT unique_userid_friendid UNIQUE (userid, friendid);

insert into connections(userid,friendid) values(1,2);
insert into connections(userid,friendid) values(2,1);
insert into connections(userid,friendid) values(1,3);

-- posts table
create table posts(
postid serial primary key,
authorid int,
title varchar(100),
description varchar(200),
created_at timestamp default now(),
CONSTRAINT fk_authorid FOREIGN KEY(authorid) REFERENCES users(userid)
);

insert into posts(authorid,title,description) values(1,'Post 1','Feeling lucky today!');
insert into posts(authorid,title,description) values(1,'Post 2','Its Saturday Night!');
insert into posts(authorid,title,description) values(2,'Post 2','Hi!');
insert into posts(authorid,title,description) values(2,'Post 3','Hello guys!');

-- like_dislike table
create table like_dislike(
l_id serial primary key,
userid int,
postid int,
status varchar(20) not null,
CONSTRAINT fk_userid FOREIGN KEY(userid) REFERENCES users(userid),
CONSTRAINT fk_postid FOREIGN KEY(postid) REFERENCES posts(postid) on delete cascade
);

ALTER TABLE like_dislike ADD CONSTRAINT unique_usrid_postid UNIQUE (userid, postid);

insert into like_dislike(userid,postid,status) values(1,3,'LIKE');
insert into like_dislike(userid,postid,status) values(1,4,'LIKE');
insert into like_dislike(userid,postid,status) values(2,1,'DISLIKE');
insert into like_dislike(userid,postid,status) values(2,2,'LIKE');

-- Comments table
create table comments(
commentid serial primary key,
userid int,
postid int,
comment varchar(100) not null,
CONSTRAINT fk_userid FOREIGN KEY(userid) REFERENCES users(userid),
CONSTRAINT fk_postid FOREIGN KEY(postid) REFERENCES posts(postid) on delete cascade
);


-- GET ALL THE TABLE NAMES -Postgresql
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public' AND table_type='BASE TABLE';












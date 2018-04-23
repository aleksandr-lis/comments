-- drop table if exists log;
-- drop table if exists comment;
-- drop table if exists article;
-- drop table if exists person;


create table article (
  id serial primary key,
  content text not null
) with (oids=false);

insert into article (content) values ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent quis odio sed sem faucibus iaculis.');


create table person (
  id serial primary key,
  sid varchar(32) not null,
  name text
) with (oids=false);

insert into person (name, sid) values ('John Doe', 'some_session_id');


create table comment (
  id serial primary key,
  parent_id integer references comment(id),
  thread_id integer references comment(id),
  article_id integer references article(id),
  person_id integer not null references person(id),
  created timestamptz not null default now(),
  content text not null,
  is_deleted bool not null default false
) with (oids=false);

insert into comment (article_id, person_id, content) values (1, 1, 'Very first comment');
insert into comment (article_id, person_id, thread_id, parent_id, content) values (1, 1, 1, 1, 'Yep, its true');
insert into comment (article_id, person_id, thread_id, parent_id, content) values (1, 1, 1, 2, 'Or not');
insert into comment (article_id, person_id, thread_id, parent_id, content) values (1, 1, 1, 2, 'Maybe');
insert into comment (article_id, person_id, thread_id, parent_id, content) values (1, 1, 1, 1, 'Liar!');
insert into comment (article_id, person_id, content) values (1, 1, 'Second comment');
insert into comment (article_id, person_id, content) values (1, 1, 'For logging');
insert into comment (article_id, person_id, content) values (1, 1, 'Four');


create table log (
  id serial primary key,
  type char(1) not null,
  person_id integer not null references person(id),
  comment_id integer not null references comment(id),
  created timestamptz not null default now(),
  before text,
  after text
) with (oids=false);

insert into log (type, person_id, comment_id, after) values ('i', 1, 7, 'For logging');
insert into log (type, person_id, comment_id, after) values ('i', 1, 8, 'Four');
insert into log (type, person_id, comment_id, before, after) values ('u', 1, 8, 'Four', 'Four 4');
insert into log (type, person_id, comment_id, before) values ('d', 1, 8, 'Four 4');
insert into log (type, person_id, comment_id, before, after) values ('u', 1, 7, 'For logging', 'For testing');

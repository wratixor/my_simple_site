
drop table if exists rmaster.zmtd_priority cascade;
CREATE TABLE rmaster.zmtd_priority (
    priority_gid int2 PRIMARY KEY,
    description varchar(32) NOT null
);

insert into rmaster.zmtd_priority (priority_gid, description) values
(1, 'Закреплённое'),
(2, 'Важное'),
(3, 'Обычное'),
(4, 'Неважное'),
(5, 'Архив');

/*
select * from zmtd_priority;
*/

drop SEQUENCE if exists rmaster.section_sq cascade;
CREATE SEQUENCE rmaster.section_sq
INCREMENT 1
START 100
MINVALUE 100
MAXVALUE 9223372036854775807
CACHE 1;

drop table if exists rmaster.sec cascade;
CREATE TABLE rmaster.sec (
    section_gid bigint NOT NULL DEFAULT nextval('section_sq'::regclass),
    curl varchar(64) UNIQUE NOT null CHECK (curl ~ '^[a-z0-9_]{3,64}$'),
    priority int2 references zmtd_priority (priority_gid),
    title varchar(64) NOT null,
    adult_flg boolean default false,
    start_date timestamptz not null default now(),
    update_date timestamptz not null default now(),
    CONSTRAINT "section$pk" PRIMARY KEY (section_gid)
);

DROP FUNCTION IF EXISTS api.s_aou_section(text, int, text, boolean, bigint);
CREATE OR REPLACE FUNCTION api.s_aou_section(i_curl_sec text, i_priority int default 5::int, i_title text default null::text, i_adult boolean default false::boolean, i_gid bigint default null::bigint)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_update boolean := false;
  l_check_available boolean := false;
  l_check_gid boolean := false;
  l_check_add boolean := false;
  l_check_curl_sec boolean := lower(i_curl_sec) ~ '^[a-z0-9_]{3,64}$';

  l_curl_sec varchar(64) := lower(i_curl_sec);
  l_title varchar(64) := coalesce(i_title, 'Untitled');
  l_adult boolean := i_adult;
  l_gid bigint := coalesce(i_gid, 0);
  l_priority int2 := i_priority;

 BEGIN

  IF l_check_curl_sec THEN
    l_check_gid := ((select count(1) from rmaster.sec where section_gid = l_gid) = 1);
    l_priority := (select case when max(priority_gid) > l_priority then l_priority else max(priority_gid) end as p from rmaster.zmtd_priority);
    l_check_available := ((select count(1) from rmaster.sec where curl = l_curl_sec) = 0);
    IF l_gid = 0 and l_check_curl_sec and l_check_available THEN
      insert into rmaster.sec (curl, priority, title, adult_flg) values (l_curl_sec, l_priority,  l_title, l_adult);
      l_check_add := true;
    ELSE
      IF l_check_gid THEN
        update rmaster.sec set curl = l_curl_sec, priority = l_priority, title = l_title, adult_flg = l_adult, update_date = now() where section_gid = l_gid;
        l_check_update = true;
      END IF;
    END IF;
  END IF;

  RETURN (
    SELECT
      case when not l_check_curl_sec then 'Недопустимый набор символов URL, допустимы a-z и _ от 3-64 символа'
           when l_check_add                            then 'Раздел добавлен /' || l_curl_sec
           when l_check_update                         then 'Раздел обновлён /' || l_curl_sec
           when l_gid > 0 and not l_check_gid then 'Отсутствует раздел #' || l_gid
           when not l_check_available then 'Раздел /'  || l_curl_sec || ' - уже существует. Задайте другой URL'
           else 'Не выполнено' end::text as status
    FOR READ ONLY
  );
 END
$function$
;


select * from api.s_aou_section('about', 5::int, 'About', false);
select * from api.s_aou_section('dev_null', 5::int, 'Архив', false);

select * from sec;


DROP TYPE IF EXISTS api.t_all_section CASCADE;
CREATE TYPE api.t_all_section AS (
	section_gid bigint,
    curl text,
	priority int,
    title text,
    adult_flg boolean,
    start_date timestamptz,
    update_date timestamptz);

DROP FUNCTION IF EXISTS api.r_all_section();
CREATE OR REPLACE FUNCTION api.r_all_section()
 RETURNS SETOF api.t_all_section
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 20
AS $function$
DECLARE

BEGIN
    RETURN QUERY
    select s.section_gid::bigint as section_gid
         , s.curl::text as curl
         , s.priority::int as priority
         , s.title::text as title
         , s.adult_flg::boolean as adult_flg
         , s.start_date::timestamptz as start_date
         , s.update_date::timestamptz as update_date
      from rmaster.sec as s
     order by s.priority, s.curl
    FOR READ ONLY;
RETURN;
END
$function$
;

select * from api.r_all_section();

DROP TYPE IF EXISTS api.t_section CASCADE;
CREATE TYPE api.t_section AS (
	curl text,
	title text,
    gid bigint);


DROP FUNCTION IF EXISTS api.r_section();
CREATE OR REPLACE FUNCTION api.r_section()
 RETURNS SETOF api.t_section
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 20
AS $function$
DECLARE

BEGIN
    RETURN QUERY
    select s.curl::text as curl
         , s.title::text as title
         , s.section_gid::bigint as gid
      from rmaster.sec as s
     order by s.priority, s.curl
    FOR READ ONLY;
RETURN;
END
$function$
;

/*
select * from api.r_section();
*/


drop SEQUENCE if exists rmaster.image_sq cascade;
CREATE SEQUENCE rmaster.image_sq
INCREMENT 1
START 100
MINVALUE 100
MAXVALUE 9223372036854775807
CACHE 1;


drop table if exists rmaster.image cascade;
CREATE TABLE rmaster.image (
    image_gid bigint NOT NULL DEFAULT nextval('image_sq'::regclass),
    curl char(32) UNIQUE NOT null,
    ext varchar(8) NOT null,
    image bytea not null,
    start_date timestamptz not null default now(),
    update_date timestamptz not null default now(),
    CONSTRAINT "image$pk" PRIMARY KEY (image_gid),
    CONSTRAINT hash_check CHECK (curl = md5(image))
);


DROP FUNCTION IF EXISTS api.s_aou_image(bytea, text, bigint);
CREATE OR REPLACE FUNCTION api.s_aou_image(i_image bytea, i_format text default 'png'::text, i_curl text default null::text)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_update boolean := false;
  l_check_available boolean := false;
  l_check_gid boolean := false;
  l_check_add boolean := false;
  l_check_curl boolean := lower(i_curl) ~ '^[0-9a-f]{32}$';

  l_format varchar(8) := lower(i_format);
  l_curl char(32) := coalesce(i_curl, '');
  l_hash char(32) := md5(i_image);

 BEGIN

  IF l_curl <> '' and l_check_curl THEN
    l_check_gid := ((select count(1) from rmaster.image where curl = l_curl) = 1);
  END IF;

  l_check_available := ((select count(1) from rmaster.image where curl = l_hash) = 0);

  IF l_check_gid and l_check_available THEN
    update rmaster.image set image = i_image, ext = l_format, curl = l_hash, update_date = now() where curl = l_curl;
    l_check_update := true;
  END IF;

  IF not l_check_gid and l_check_available THEN
    insert into rmaster.image (image, ext, curl)
                       values (i_image, l_format, l_hash);
    l_check_add := true;
  END IF;

  RETURN (
    SELECT
      case when l_check_add                            then 'Загружено изображение /' || l_hash
           when l_check_update                         then 'Обновлено изображение /' || l_hash
           when l_curl <> '' and not l_check_gid       then 'Отсутствует изображение /' || l_curl
           when not l_check_available                  then 'Изображение /' || l_hash || ' уже есть в базе.'
           else 'Не выполнено' end::text as status
    FOR READ ONLY
  );
 END
$function$
;


select * from api.s_aou_image('\x89504e470d0a1a0a0000000d4948445200000040000000400802000000250be689000000017352474200aece1ce90000000467414d410000b18f0bfc6105000000097048597300000ec300000ec301c76fa86400000023494441546843edc1010d000000c2a0f74f6d0f070400000000000000000000009cab01304000010c606ff50000000049454e44ae426082'::bytea);

/*
select * from image;
select image::text from image where curl = '3177c2b93127d51fa22b9e043839e89c';
*/

DROP TYPE IF EXISTS api.t_all_images CASCADE;
CREATE TYPE api.t_all_images AS (
    curl text,
    etc text,
    gid bigint);


DROP FUNCTION IF EXISTS api.r_all_images();
CREATE OR REPLACE FUNCTION api.r_all_images()
 RETURNS SETOF api.t_all_images
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 40
AS $function$
DECLARE

BEGIN
    RETURN QUERY
    select s.curl::text as curl
         , ('.' || s.ext || ' (' || to_char(s.start_date, 'DD.MM.YYYY, HH24:MI:SS') || ' / ' || to_char(s.update_date, 'DD.MM.YYYY, HH24:MI:SS') || ')')::text as etc
         , s.image_gid::bigint as gid
      from rmaster.image as s
     order by s.update_date desc
    FOR READ ONLY;
RETURN;
END
$function$
;

select * from api.r_all_images();

DROP TYPE IF EXISTS api.t_image CASCADE;
CREATE TYPE api.t_image AS (
    image bytea,
    ext text);

DROP FUNCTION IF EXISTS api.r_image(text);
CREATE OR REPLACE FUNCTION api.r_image(i_curl text default null::text)
 RETURNS SETOF api.t_image
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 1
AS $function$
DECLARE
 l_check_curl_img boolean := lower(i_curl) ~ '^[0-9a-f]{32}$';
 l_curl_img char(32) := lower(i_curl);
 l_check_img boolean := false;
 l_gid bigint := 0;
BEGIN
  IF l_check_curl_img THEN
    l_check_img := ((select count(1) from rmaster.image where curl = l_curl_img) = 1);
  END IF;
  IF l_check_img THEN
    l_gid := (select image_gid from rmaster.image where curl = l_curl_img);
  ELSE
    l_gid := (select image_gid from rmaster.image where curl = '3177c2b93127d51fa22b9e043839e89c');
  END IF;
  RETURN QUERY
    select s.image::bytea as image
         , lower(s.ext)::text as ext
      from rmaster.image as s
     where s.image_gid = l_gid
    FOR READ ONLY;
RETURN;
END
$function$
;

/*
select * from api.r_image();
select * from api.r_image('3177c2b93127d51fa22b9e043839e89c'::text);
select * from api.r_image('53f5a970493be6b35bb5d3f127e9245b'::text);
select * from api.r_image('df9dcbf3646787209973a055ee92bfc3'::text);
*/

drop SEQUENCE if exists rmaster.chapter_sq cascade;
CREATE SEQUENCE rmaster.chapter_sq
INCREMENT 1
START 100
MINVALUE 100
MAXVALUE 9223372036854775807
CACHE 1;

drop table if exists rmaster.chapter cascade;
CREATE TABLE rmaster.chapter (
    chapter_gid bigint NOT NULL DEFAULT nextval('chapter_sq'::regclass),
    curl varchar(64) UNIQUE NOT null CHECK (curl ~ '^[a-z0-9_]{3,64}$'),
    priority int2 references zmtd_priority (priority_gid),
    section_gid bigint references sec (section_gid),
    image_gid bigint references image (image_gid),
    thumb_image_gid bigint references image (image_gid),
    title varchar(64) NOT null,
    adult_flg boolean default false,
    center_flg boolean default false,
    article text,
    start_date timestamptz not null default now(),
    update_date timestamptz not null default now(),
    CONSTRAINT "chapter$pk" PRIMARY KEY (chapter_gid)
);


DROP FUNCTION IF EXISTS api.s_aou_chapter(text, text, text, int4, text, text, text, bool, bool, int8);
CREATE OR REPLACE FUNCTION api.s_aou_chapter(i_curl_sec text, i_curl_chap text, i_article text, i_priority int default 5::int, i_title text default null::text
                                            , i_curl_img_t text default null::text, i_curl_img text default null::text, i_center boolean default false::boolean
                                            , i_adult boolean default false::boolean, i_gid bigint default null::bigint)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_update boolean := false;
  l_check_gid boolean := false;
  l_check_add boolean := false;
  l_check_curl_sec boolean := lower(i_curl_sec) ~ '^[a-z0-9_]{3,64}$';
  l_check_curl_chap boolean := lower(i_curl_chap) ~ '^[a-z0-9_]{3,64}$';
  l_check_curl_img_t boolean := lower(i_curl_img_t) ~ '^[0-9a-f]{32}$';
  l_check_curl_img boolean := lower(i_curl_img) ~ '^[0-9a-f]{32}$';
  l_check_available boolean := false;
  l_check_current boolean := false;

  l_curl_sec varchar(64) := lower(i_curl_sec);
  l_curl_chap varchar(64) := lower(i_curl_chap);
  l_curl_img_t char(32) := lower(i_curl_img_t);
  l_curl_img char(32) := lower(i_curl_img);
  l_title varchar(64) := coalesce(i_title, 'Untitled');
  l_article text := i_article;
  l_adult boolean := i_adult;
  l_center boolean := i_center;
  l_gid bigint := coalesce(i_gid, 0);
  l_priority int2 := i_priority;

  l_image_gid bigint := null;
  l_thumb_image_gid bigint := null;
  l_section_gid bigint := null;

 BEGIN

  IF l_check_curl_sec THEN
    l_check_gid := ((select count(1) from rmaster.chapter where chapter_gid = l_gid) = 1);
    l_priority := (select case when max(priority_gid) > l_priority then l_priority else max(priority_gid) end as p from rmaster.zmtd_priority);
    l_check_available := ((select count(1) from rmaster.chapter where curl = l_curl_chap) = 0);
    l_check_current := ((select count(1) from rmaster.chapter where curl = l_curl_chap and chapter_gid = l_gid) = 1);

    IF l_check_curl_sec THEN
      l_section_gid := (select section_gid from rmaster.sec where curl = l_curl_sec);
    END IF;
    IF l_check_curl_img THEN
      l_image_gid := (select image_gid from rmaster.image where curl = l_curl_img);
    END IF;
    IF l_check_curl_img_t THEN
      l_thumb_image_gid := (select image_gid from rmaster.image where curl = l_curl_img_t);
    END IF;
    IF not l_adult and l_section_gid is not null THEN
      l_adult = (select adult_flg from rmaster.sec where section_gid = l_section_gid);
    END IF;

    IF l_check_curl_chap and l_section_gid is not null THEN
      IF l_gid = 0 and l_check_available  THEN
        insert into rmaster.chapter (curl, priority, section_gid, image_gid, thumb_image_gid, title, article, adult_flg, center_flg)
                             values (l_curl_chap, l_priority, l_section_gid, l_image_gid, l_thumb_image_gid, l_title, l_article, l_adult, l_center);
        l_check_add := true;
      ELSE
        IF l_check_gid and (l_check_available or l_check_current) THEN
          update rmaster.chapter set curl = l_curl_chap, priority = l_priority
                                   , section_gid = l_section_gid, image_gid = l_image_gid
                                   , thumb_image_gid = l_thumb_image_gid, title = l_title
                                   , article = l_article, adult_flg = l_adult
                                   , center_flg = l_center, update_date = now()
                               where chapter_gid = l_gid;
          l_check_update = true;
        END IF;
      END IF;
    END IF;
  END IF;

  RETURN (
    SELECT
      case when not l_check_curl_sec                       then 'Недопустимый набор символов URL, допустимы a-z и _ от 3-64 символа'
           when l_section_gid is null                      then 'Раздел /' || l_curl_sec || ' - не существует'
           when l_check_add                                then 'Статья добавлена /' || l_curl_sec || '/' || l_curl_chap
           when l_check_update                             then 'Статья обновлена /' || l_curl_sec || '/' || l_curl_chap
           when l_gid > 0 and not l_check_gid              then 'Отсутствует статья #' || l_gid
           when not (l_check_available or l_check_current) then 'Статья /' || l_curl_chap || ' - уже существует или не соответствует номеру #' || l_gid || '. Задайте другой URL'
           else 'Не выполнено' end::text as status
    FOR READ ONLY
  );
 END
$function$
;

select * from api.s_aou_chapter('dev_null'::text
                               , 'void_2'::text
                               , '<b>Void</b><br><code>public static void</code><br><p>Default void page</p><p>lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet!</p>'::text
                               , 5::int
                               , 'Void'::text
                               , '3177c2b93127d51fa22b9e043839e89c'::text
                               , '3177c2b93127d51fa22b9e043839e89c'::text);

select * from api.s_aou_chapter('dev_null'::text
                               , 'dev_null'::text
                               , '<h2>/dev/null</h2>'::text
                               , 5::int
                               , 'Null'::text
                               , 'i_curl_img_t'::text
                               , 'i_curl_img'::text
                               , true::boolean
                               , false::boolean
                               , null::bigint);

select * from api.s_aou_chapter('about'::text
                               , 'important'::text
                               , '<h2>Важная заглушка для тестов</h2>'::text
                               , 1::int
                               , 'Заглушка'::text
                               , 'i_curl_img_t'::text
                               , 'i_curl_img'::text
                               , true::boolean
                               , false::boolean
                               , null::bigint);

select * from api.s_aou_chapter('dev_null'::text
                               , 'important_2'::text
                               , '<h2>Важная заглушка для тестов</h2>'::text
                               , 1::int
                               , 'Заглушка'::text
                               , 'i_curl_img_t'::text
                               , 'i_curl_img'::text
                               , true::boolean
                               , false::boolean
                               , null::bigint);

/*
select * from rmaster.chapter;
*/

DROP FUNCTION IF EXISTS api.s_crop(text);
CREATE OR REPLACE FUNCTION api.s_crop(i_text text)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_text text := substring(regexp_replace(i_text, '<.*?>', ' ', 'g') from 0 for 200);
 BEGIN
  RETURN l_text;
 END
$function$
;



DROP TYPE IF EXISTS api.t_all_chapter CASCADE;
CREATE TYPE api.t_all_chapter AS (
    curl text,
	imageid text,
    item text,
	chapter_gid bigint);

DROP FUNCTION IF EXISTS api.r_all_chapter(text);
CREATE OR REPLACE FUNCTION api.r_all_chapter(i_curl_sec text)
 RETURNS SETOF api.t_all_chapter
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 20
AS $function$
DECLARE
  l_check_curl_sec boolean := lower(i_curl_sec) ~ '^[a-z0-9_]{3,64}$';
  l_curl_sec varchar(64) := lower(i_curl_sec);
  l_section_gid bigint := null;

BEGIN
    IF l_check_curl_sec THEN
      l_section_gid := (select section_gid from rmaster.sec where curl = l_curl_sec);
    END IF;
    RETURN QUERY
        select curl, imageid, item, chapter_gid from (
	    select (s.curl || '/' || c.curl)::text as curl
	         , i.curl::text as imageid
	         , ('<b>' || c.title || '</b><br>' || '<i>' || to_char(c.update_date, 'DD.MM.YYYY, HH24:MI:SS') || '</i><br>' || api.s_crop(c.article))::text as item
             , c.chapter_gid::bigint as chapter_gid
             , c.priority
             , c.update_date
	      from rmaster.chapter as c
          join rmaster.sec as s on s.section_gid = c.section_gid
          left join rmaster.image as i on i.image_gid = c.thumb_image_gid
         where s.section_gid = l_section_gid
         union
	    select (s.curl || '/' || c.curl)::text as curl
	         , i.curl::text as imageid
	         , ('<b>' || c.title || '</b><br>' || '<i>' || to_char(c.update_date, 'DD.MM.YYYY, HH24:MI:SS') || '</i><br>' || api.s_crop(c.article))::text as item
             , c.chapter_gid::bigint as chapter_gid
             , c.priority
             , c.update_date
	      from rmaster.chapter as c
          join rmaster.sec as s on s.section_gid = c.section_gid
          left join rmaster.image as i on i.image_gid = c.thumb_image_gid
	     where l_section_gid is null and c.priority = 1::int2
         ) t
         order by t.priority, t.update_date desc
    FOR READ ONLY;
RETURN;
END
$function$
;

select * from api.r_all_chapter('dev_null'::text);
select * from api.r_all_chapter('all'::text);

DROP TYPE IF EXISTS api.t_chapter CASCADE;
CREATE TYPE api.t_chapter AS (
	flg_center boolean,
	imageid text,
	article text,
    gid bigint);

DROP FUNCTION IF EXISTS api.r_chapter(text);
CREATE OR REPLACE FUNCTION api.r_chapter(i_curl_chap text)
 RETURNS SETOF api.t_chapter
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 1
AS $function$
DECLARE
  l_check_curl_chap boolean := lower(i_curl_chap) ~ '^[a-z0-9_]{3,64}$';
  l_curl_chap varchar(64) := lower(i_curl_chap);
  l_chapter_gid bigint := null;

BEGIN
    IF l_check_curl_chap THEN
      l_chapter_gid := (select chapter_gid from rmaster.chapter where curl = l_curl_chap);
    END IF;
    RETURN QUERY
	    select c.center_flg::boolean as flg_center
	         , i.curl::text as imageid
	         , (c.article || '<br><br><br><i>' || to_char(c.start_date, 'DD.MM.YYYY, HH24:MI:SS') || ' / ' || to_char(c.update_date, 'DD.MM.YYYY, HH24:MI:SS') || '</i><br>' )::text as article
             , c.chapter_gid::bigint as gid
	      from rmaster.chapter as c
	      left join rmaster.image as i on i.image_gid = c.image_gid
	     where l_chapter_gid is not null
	       and c.chapter_gid = l_chapter_gid
	     union
	    select true as flg_center
	         , null::text as imageid
	         , ('<h1>#404</h1><h2>Такой страницы нет!</h2><h3>Проверьте адрес или попробуйте ещё раз...</h3>')::text as article
             , 0::bigint as gid
	      from (select 1) s
	     where l_chapter_gid is null
    FOR READ ONLY;
RETURN;
END
$function$
;
/*
api.s_aou_chapter(i_curl_sec text, i_curl_chap text, i_article text, i_priority int default 5::int, i_title text default null::text
                 , i_curl_img_t text default null::text, i_curl_img text default null::text, i_center boolean default false::boolean
                 , i_adult boolean default false::boolean, i_gid bigint default null::bigint)
*/
DROP TYPE IF EXISTS api.t_raw_chapter CASCADE;
CREATE TYPE api.t_raw_chapter AS (
	curl_sec text,
	curl text,
	article text,
	priority int,
	title text,
	curl_img_t text,
	curl_img text,
	center_f boolean,
	adult boolean,
    gid bigint);

DROP FUNCTION IF EXISTS api.r_raw_chapter(text);
CREATE OR REPLACE FUNCTION api.r_raw_chapter(i_curl_chap text)
 RETURNS SETOF api.t_raw_chapter
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 1
AS $function$
DECLARE
  l_check_curl_chap boolean := lower(i_curl_chap) ~ '^[a-z0-9_]{3,64}$';
  l_curl_chap varchar(64) := lower(i_curl_chap);
  l_chapter_gid bigint := null;

BEGIN
    IF l_check_curl_chap THEN
      l_chapter_gid := (select chapter_gid from rmaster.chapter where curl = l_curl_chap);
    END IF;
    RETURN QUERY
        select s.curl::text as curl_sec
             , c.curl::text as curl
             , c.article::text as article
             , c.priority::int as priority
             , c.title::text as title
             , ti.curl::text as curl_img_t
             , i.curl::text as curl_img
             , c.center_flg::boolean as center_f
             , c.adult_flg::boolean as adult
             , c.chapter_gid::bigint as gid
	      from rmaster.chapter as c
	      join rmaster.sec as s on s.section_gid = c.section_gid
	      left join rmaster.image as i on i.image_gid = c.image_gid
	      left join rmaster.image as ti on ti.image_gid = c.thumb_image_gid
	     where l_chapter_gid is not null
	       and c.chapter_gid = l_chapter_gid
	     union
	    select ''::text as curl_sec
             , ''::text as curl
             , ''::text as article
             , 3::int as priority
             , ''::text as title
             , ''::text as curl_img_t
             , ''::text as curl_img
             , false::boolean as center
             , false::boolean as adult
             , 0::bigint as gid
	      from (select 1) s
	     where l_chapter_gid is null
    FOR READ ONLY;
RETURN;
END
$function$
;

/*
select * from api.r_chapter('important'::text);

select * from rmaster.chapter;
*/

drop SEQUENCE if exists rmaster.title_sq cascade;
CREATE SEQUENCE rmaster.title_sq
INCREMENT 1
START 100
MINVALUE 100
MAXVALUE 9223372036854775807
CACHE 1;

drop table if exists rmaster.title cascade;
CREATE TABLE rmaster.title (
    title_gid bigint NOT NULL DEFAULT nextval('title_sq'::regclass),
    title varchar(64) unique NOT null,
    CONSTRAINT "title$pk" PRIMARY KEY (title_gid)
);

DROP FUNCTION IF EXISTS api.s_aou_title(text, bigint);
CREATE OR REPLACE FUNCTION api.s_aou_title(i_title text, i_gid bigint default null::bigint)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_update boolean := false;
  l_check_available boolean := false;
  l_check_gid boolean := false;
  l_check_add boolean := false;

  l_title varchar(64) := coalesce(i_title, 'Untitled');
  l_gid bigint := coalesce(i_gid, 0);

 BEGIN

  l_check_available := ((select count(1) from rmaster.title where title = l_title) = 0);
  l_check_gid := ((select count(1) from rmaster.title where title_gid = l_gid) = 1);
  IF l_check_available THEN
    IF l_gid = 0 THEN
      insert into rmaster.title (title) values (l_title);
      l_check_add := true;
    ELSE
      IF l_check_gid THEN
        update rmaster.title set title = l_title where title_gid = l_gid;
        l_check_update = true;
      END IF;
    END IF;
  END IF;

  RETURN (
    SELECT
      case when l_check_add                   then 'Заголовок добавлен: ' || l_title
           when l_check_update                then 'Заголовок обновлён: ' || l_title
           when l_gid > 0 and not l_check_gid then 'Отсутствует заголовок #' || l_gid
           when not l_check_available         then 'Заголовок "'  || l_title || '" - уже существует'
           else 'Не выполнено' end::text as status
    FOR READ ONLY
  );
 END
$function$
;

select * from api.s_aou_title('Личный сайт кодера-стихоплюя'::text);
select * from api.s_aou_title('Никто не просил, а я сделал'::text);
select * from api.s_aou_title('Приветствуем заблудших!'::text);
select * from api.s_aou_title('Дизайн разработан профессиональными программистами'::text);
select * from api.s_aou_title('Доброго времени суток, странник...'::text);
select * from api.s_aou_title('Партенофобия и борщ'::text);
select * from api.s_aou_title('Надеюсь, ты найдёшь, что ищешь...'::text);
select * from api.s_aou_title('test'::text);

DROP FUNCTION IF EXISTS api.s_rnd_title();
CREATE OR REPLACE FUNCTION api.s_rnd_title()
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE

 BEGIN
  RETURN (select title::text from rmaster.title order by random() limit 1);
 END
$function$
;

/*
select * from api.s_rnd_title();
select * from api.s_rnd_title();
select * from api.s_rnd_title();
select * from api.s_rnd_title();
*/

DROP TYPE IF EXISTS api.t_all_title CASCADE;
CREATE TYPE api.t_all_title AS (
    title text,
    gid bigint);


DROP FUNCTION IF EXISTS api.r_all_title();
CREATE OR REPLACE FUNCTION api.r_all_title()
 RETURNS SETOF api.t_all_title
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 20
AS $function$
DECLARE

BEGIN
    RETURN QUERY
    select t.title::text as title
         , t.title_gid::bigint as gid
      from rmaster.title as t
     order by t.title_gid desc
    FOR READ ONLY;
RETURN;
END
$function$
;

/*
select * from api.r_all_title();
*/

DROP TYPE IF EXISTS api.t_page CASCADE;
CREATE TYPE api.t_page AS (
	adult boolean,
	title text,
	curl text);

DROP FUNCTION IF EXISTS api.r_page(text, text);
CREATE OR REPLACE FUNCTION api.r_page(i_curl_sec text, i_curl_chap text)
 RETURNS SETOF api.t_page
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER COST 1 ROWS 1
AS $function$
DECLARE
  l_check_curl_chap boolean := lower(i_curl_chap) ~ '^[a-z0-9_]{3,64}$';
  l_check_curl_sec boolean := lower(i_curl_sec) ~ '^[a-z0-9_]{3,64}$';
  l_curl_chap varchar(64) := lower(i_curl_chap);
  l_curl_sec varchar(64) := lower(i_curl_sec);
  l_chapter_gid bigint := null;
  l_section_gid bigint := null;


BEGIN
    IF l_check_curl_sec THEN
      l_section_gid := (select section_gid from rmaster.sec where curl = l_curl_sec);
    END IF;
    IF l_check_curl_chap THEN
      l_chapter_gid := (select chapter_gid from rmaster.chapter where curl = l_curl_chap);
    END IF;
    RETURN QUERY
	    select (c.adult_flg or s.adult_flg)::boolean as adult
	         , (s.title || ': ' || c.title)::text as title
             , ('/' || s.curl || '/' || c.curl)::text as curl
	      from rmaster.chapter as c
          join rmaster.sec as s on c.section_gid = s.section_gid
	     where l_chapter_gid is not null
	       and c.chapter_gid = l_chapter_gid
	     union
        select (s.adult_flg)::boolean as adult
	         , ('Wratixor.ru — ' || s.title)::text as title
             , ('/' || s.curl)::text as curl
	      from rmaster.sec as s
	     where l_chapter_gid is null
           and l_section_gid is not null
	       and s.section_gid = l_section_gid
	     union
        select (false)::boolean as adult
	         , ('Wratixor.ru — ' || api.s_rnd_title()::text)::text as title
             , ('')::text as curl
	      from (values(1)) s
	     where l_chapter_gid is null
           and l_section_gid is null
    FOR READ ONLY;
RETURN;
END
$function$
;

/*
select * from api.r_page(null, null);
select * from api.r_page('dev_null'::text, null);
select * from api.r_page('dev_null'::text, 'important_2'::text);
*/

DROP FUNCTION IF EXISTS api.s_drop(text, bigint);
CREATE OR REPLACE FUNCTION api.s_drop(i_tablename text, i_gid bigint)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_gid boolean := false;
  l_check_drop boolean := false;

  l_tablename text := coalesce(i_tablename, 'not');
  l_gid bigint := coalesce(i_gid, 0);

 BEGIN

  IF l_tablename in ('section', 'sec') THEN
    l_check_gid := ((select count(1) from rmaster.sec where section_gid = l_gid) = 1);
    IF l_check_gid THEN
      delete from rmaster.sec where section_gid = l_gid;
      l_check_drop := true;
    END IF;
  END IF;
  IF l_tablename in ('chapter', 'chap') THEN
    l_check_gid := ((select count(1) from rmaster.chapter where chapter_gid = l_gid) = 1);
    IF l_check_gid THEN
      delete from rmaster.chapter where chapter_gid = l_gid;
      l_check_drop := true;
    END IF;
  END IF;
  IF l_tablename in ('image', 'img')  THEN
    l_check_gid := ((select count(1) from rmaster.image where image_gid = l_gid) = 1);
    IF l_check_gid THEN
      delete from rmaster.image where image_gid = l_gid;
      l_check_drop := true;
    END IF;
  END IF;
  IF l_tablename in ('title', 't') THEN
    l_check_gid := ((select count(1) from rmaster.title where title_gid = l_gid) = 1);
    IF l_check_gid THEN
      delete from rmaster.title where title_gid = l_gid;
      l_check_drop := true;
    END IF;
  END IF;


  RETURN (
    SELECT
      case when l_check_drop                  then 'Удалено #' || l_gid ||' из .' || l_tablename
           when l_gid > 0 and not l_check_gid then 'Отсутствует #' || l_gid || ' в .' || l_tablename
           else 'Не выполнено' end::text as status
    FOR READ ONLY
  );
 END
$function$
;


select * from api.s_drop('t'::text, 107::bigint);


drop table if exists rmaster.auth cascade;
CREATE TABLE rmaster.auth (
    login varchar(64) NOT NULL,
    passhash char(32) NOT null,
    admin_flg boolean NOT null,
    session_gid char(32)  null,
    CONSTRAINT "auth$pk" PRIMARY KEY (login)
);


DROP FUNCTION IF EXISTS api.s_get_hash(text, text);
CREATE OR REPLACE FUNCTION api.s_get_hash(i_login text, i_pass text)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_salt text := 'LoremIpsumDolorSitAmet';
  l_hash char(32) := md5(i_login || i_pass || l_salt);
 BEGIN
  RETURN (l_hash);
 END
$function$
;

/*
select * from api.s_get_hash('vasya'::text, to_char(now(), 'YYYYMMDDHH24MISSMSUS')::text);
*/

DROP FUNCTION IF EXISTS api.s_aou_auth(text, text, text);
CREATE OR REPLACE FUNCTION api.s_aou_auth(i_login text, i_pass text, i_new_pass text)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_update boolean := false;
  l_check_available boolean := false;
  l_check_add boolean := false;
  l_check_new_admin boolean := false;
  l_check_correct boolean := false;
  l_check_reg boolean := i_pass = i_new_pass;
  l_check_login boolean := i_login ~ '^[a-zA-Z0-9_]{3,64}$';
  l_check_pass boolean := i_pass ~ '^....*$';
  l_check_npass boolean := i_new_pass ~ '^....*$';

  l_login varchar(64) := i_login;
  l_pass char(32) := api.s_get_hash(l_login::text, i_pass::text);
  l_npass char(32) := api.s_get_hash(l_login::text, i_new_pass::text);

 BEGIN

  IF l_check_login and l_check_pass THEN
     l_check_new_admin := (((select count(1) from rmaster.auth) = 0) and l_check_reg);
     IF l_check_reg THEN
        l_check_available := ((select count(1) from rmaster.auth where login = l_login) = 0);
        IF l_check_available THEN
           insert into rmaster.auth (login, passhash, admin_flg)
                             values (l_login, l_pass, l_check_new_admin);
           l_check_add := true;
        END IF;
     ELSE
        IF l_check_npass THEN
           l_check_correct := ((select count(1) from rmaster.auth where login = l_login and passhash = l_pass) = 1);
           IF l_check_correct THEN
              update rmaster.auth set passhash = l_npass where login = l_login;
              l_check_update := true;
           END IF;
        END IF;
     END IF;
  END IF;

  RETURN (
    SELECT
      case when     l_check_add                        then 'register'
           when     l_check_update                     then 'update'
           when not l_check_available and l_check_reg  then 'no_available_login'
           when not l_check_login                      then 'incorrect_login'
           when not l_check_pass                       then 'short_password'
           when not l_check_npass                      then 'short_new_password'
           when not l_check_correct                    then 'incorrect_login_or_password'
           else 'do_nothing' end::text as status
    FOR READ ONLY
  );
 END
$function$
;


DROP FUNCTION IF EXISTS api.s_set_auth(text, text);
CREATE OR REPLACE FUNCTION api.s_set_auth(i_login text, i_pass text)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_correct boolean := false;
  l_check_login boolean := i_login ~ '^[a-zA-Z0-9_]{3,64}$';
  l_check_pass boolean := i_pass ~ '^....*$';

  l_login varchar(64) := i_login;
  l_pass char(32) := api.s_get_hash(l_login::text, i_pass::text);

  l_session char(32) := api.s_get_hash(l_login::text, to_char(now(), 'YYYYMMDDHH24MISSMSUS')::text);

 BEGIN

  IF l_check_login and l_check_pass THEN
     l_check_correct := ((select count(1) from rmaster.auth where login = l_login and passhash = l_pass) = 1);
     IF l_check_correct THEN
        update rmaster.auth set session_gid = l_session where login = l_login;
     END IF;
  END IF;

  RETURN (
    SELECT
      case when not l_check_login                      then 'incorrect_login'
           when not l_check_pass                       then 'short_password'
           when not l_check_correct                    then 'incorrect_login_or_password'
           else l_session end::text as status
    FOR READ ONLY
  );
 END
$function$
;



DROP FUNCTION IF EXISTS api.s_get_auth(text, text);
CREATE OR REPLACE FUNCTION api.s_get_auth(i_login text, i_session text)
 RETURNS text
 LANGUAGE plpgsql
 VOLATILE SECURITY DEFINER COST 1
AS $function$
 DECLARE
  l_check_correct boolean := false;
  l_check_admin   boolean := false;
  l_check_login   boolean := i_login ~ '^[a-zA-Z0-9_]{3,64}$';
  l_check_session boolean := i_session ~ '^[0-9a-f]{32}$';

  l_login varchar(64) := i_login;
  l_session  char(32) := i_session;

 BEGIN

  IF l_check_login and l_check_session THEN
     l_check_correct := ((select count(1) from rmaster.auth where login = l_login and session_gid = l_session) = 1);
     IF l_check_correct THEN
        l_check_admin := (select admin_flg from rmaster.auth where login = l_login);
     END IF;
  END IF;

  IF l_check_login and not l_check_correct THEN
     update rmaster.auth set session_gid = null where login = l_login;
  END IF;

  RETURN (
    SELECT case when     l_check_admin                      then 'admin'
                when not l_check_admin and l_check_correct  then 'user'
                when not l_check_login                      then 'incorrect_login'
                when not l_check_correct and l_check_login  then 'reset_session'
                else 'anon' end::text as status
    FOR READ ONLY
  );
 END
$function$
;

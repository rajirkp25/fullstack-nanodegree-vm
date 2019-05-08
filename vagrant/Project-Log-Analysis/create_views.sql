--materialized views and indexes for project log analysis

 create materialized view log_count_status_path as
 select path, count(path) , status , 
 substr(upper(replace(substring(path, position('e/' in path)+2, char_length(path)  ), '-',' ')),1,3) TITLE_UPPER,
 upper(substring(path, position('e/' in path)+2, char_length(path)  )) slug_upper
from log group by path , status, substr(upper(replace(substring(path, position('e/' in path)+2, char_length(path)  ), '-',' ')),1,3),
upper(substring(path, position('e/' in path)+2, char_length(path)  )) 
 order by count desc;

 CREATE INDEX  slug_idx ON log_count_status_path (slug_upper);

 create materialized view author_articles as
  select a.name, a.id author_id, b.title, b.author, b.id article_id,  b.slug, upper(b.slug) slug_upper, upper(substr(b.title,1,3)) TITLE_UPPER
  from authors a, articles b where a.id=b.author order by a.id;


  CREATE INDEX  slug_upper_idx ON author_articles (slug_upper);

create materialized view  log_err_date as
select time::timestamp::date as err_date, COUNT(1) AS total_logs,
SUM( CASE WHEN status !=  '200 OK' THEN 1 ELSE 0 END) AS not_ok_logs
from log GROUP BY err_date  ORDER BY err_date ASC;
# Project Title

**Project: Logs Analysis**

## Getting Started

This python program will be run against the "news" database and prints a report of

- The most popular three articles of all time
- The most popular article authors of all time
- On which days did more than 1% of requests lead to errors?

The python program has 3 below functions, that prints the reports respectively

1. get_popular_articles
2. get_popular_authors
3. get_err_days

## Requirements

- Vagrant
- VirtualBox
- Vagrant file as provided by Udacity
- Python
- PostgreSQL
- psycopg2 library

## Prerequisites

<b>Assuming that Virtual Box and Udacity Vagrant are setup. For more info please check Udacity Course Installing the Virtual Machine</b>

- Vagrant can be downloaded from [Vagrant](https://www.vagrantup.com/) website
- Installing the Virtual Machine step by step guide provided at [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- Vagrant File is located in the zip file named as Vagrantfile

## Database

User can download news DB from [Here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Once the zip file is loaded and sql file extracted, DB can be imported using below command

```
  psql -d news -f <news .sql newsdata.sql
```

Python Program will connect to "news" database to run the sqls for the reports.

<b> The news DB has below objects </b>

| Schema | Name                  | Type              | Owner   |
| ------ | --------------------- | ----------------- | ------- |
| public | articles              | table             | vagrant |
| public | articles_id_seq       | sequence          | vagrant |
| public | author_articles       | materialized view | vagrant |
| public | authors               | table             | vagrant |
| public | authors_id_seq        | sequence          | vagrant |
| public | log                   | table             | vagrant |
| public | log_count_status_path | materialized view | vagrant |
| public | log_err_date          | materialized view | vagrant |
| public | log_id_seq            | sequence          | vagrant |
| public | log_with_article      | table             | vagrant |

1. Articles table stores the article info like author, title, slug, lead, body, time and id

2. Authors table stores name, bio and id of the authors

3. id of the author is stored in articles.author column as a foreign key reference

4. Log table stores the log path, ip, method of access, status of the access, time and id

5. Log.path column has the value of articles.slug, but is stored as a substring log.path value = "/article/candidate-is-jerk" where candidate-is-jerk is the value stored in articles.slug

6. The sequences comes with the news db sql file, and are used to generate unique identifiers

7. The materialized views author_articles, log_count_status_path and log_err_date are created for this project log analysis and is not part of the original news database provided by Udacity

<p>Since the log table is very big and contains 1677735 rows, writing a simple sql to get above reports would be challenging.
To make simpler sqls and database queries to run faster, materialized views and indexes are created. </p>

<i>create_views.sql attached to the zip file for easy reference to the materialized views creation. Below details on each materialized view </i>

#### Materialized View - log_count_status_path

This view is for getting the log count grouped by path, status and also to derive the slug_upper value from the path column in log table. slug_upper column gets the upper case value of the article's slug value from path column. Additionally this view also gets the first 3 letters of the slug value from path column in upper case. The title first 3 characters is not used any of the sqls used for report. This "TITLE" column is mainly for validating if the sqls are selecting the correct rows

```
create materialized view log_count_status_path as
select path, count(path) , status , substr(upper(replace(substring(path, position('e/' in path)+2, char_length(path) ), '-',' ')),1,3) TITLE_UPPER,
upper(substring(path, position('e/' in path)+2, char_length(path) )) slug_upper
from log group by path , status, substr(upper(replace(substring(path, position('e/' in path)+2, char_length(path) ), '-',' ')),1,3),
upper(substring(path, position('e/' in path)+2, char_length(path) ))
order by count desc;
```

Below INDEX creates an index of slug_upper column in the materialized view log_count_status_path. This enables easy retreival of data for the first 2 reports in this project.

```
CREATE INDEX slug_idx ON log_count_status_path (slug_upper);
```

##### Running the Select on log_count_status_path materialized view

| Path                               | Count  | Ststus        | TILE | SLUG                      |
| ---------------------------------- | ------ | ------------- | ---- | ------------------------- |
| /                                  | 479121 | 200 OK        |      |
| /article/candidate-is-jerk         | 338647 | 200 OK        | CAN  | CANDIDATE-IS-JERK         |
| /article/bears-love-berries        | 253801 | 200 OK        | BEA  | BEARS-LOVE-BERRIES        |
| /article/bad-things-gone           | 170098 | 200 OK        | BAD  | BAD-THINGS-GONE           |
| /article/goats-eat-googles         | 84906  | 200 OK        | GOA  | GOATS-EAT-GOOGLES         |
| /article/trouble-for-troubled      | 84810  | 200 OK        | TRO  | TROUBLE-FOR-TROUBLED      |
| /article/balloon-goons-doomed      | 84557  | 200 OK        | BAL  | BALLOON-GOONS-DOOMED      |
| /article/so-many-bears             | 84504  | 200 OK        | SO   | SO-MANY-BEARS             |
| /article/media-obsessed-with-bears | 84383  | 200 OK        | MED  | MEDIA-OBSESSED-WITH-BEARS |
| /spam-spam-spam-humbug             | 301    | 404 NOT FOUND | SPA  | SPAM-SPAM-SPAM-HUMBUG     |

.................

#### Materialized View - author_articles

This materialized view creates a view from tables author and articles. selecting the slog value from articles in upper case, and first 3 letters of articles in upper case.
The title first 3 characters is not used any of the sqls used for report. This "TITLE" column is mainly for validating if the sqls are selecting teh correct rows

```

create materialized view author_articles as
select a.name, a.id author_id, b.title, b.author, b.id article_id, b.slug, upper(b.slug) slug_upper, upper(substr(b.title,1,3)) TITLE_UPPER
from authors a, articles b where a.id=b.author order by a.id;
```

Below INDEX creates an index of slug_upper column in the materialized view author_articles. This enables easy retreival of data for the first 2 reports in this project.

```
CREATE INDEX slug_upper_idx ON author_articles (slug_upper);
```

##### Running the Select on author_articles materialized view

| Author                 | Author_ID | Article_Title                      | Article_Author_ID | Article_ID | Slug                      | Slug_upper                | Title_Upper |
| ---------------------- | --------- | ---------------------------------- | ----------------- | ---------- | ------------------------- | ------------------------- | ----------- |
| Ursula La Multa        | 1         | There are a lot of bears           | 1                 | 29         | so-many-bears             | SO-MANY-BEARS             | THE         |
| Ursula La Multa        | 1         | Bears love berries, alleges bear   | 1                 | 25         | bears-love-berries        | BEARS-LOVE-BERRIES        | BEA         |
| Ursula La Multa        | 1         | Goats eat Google's lawn            | 1                 | 27         | goats-eat-googles         | GOATS-EAT-GOOGLES         | GOA         |
| Ursula La Multa        | 1         | Media obsessed with bears          | 1                 | 28         | media-obsessed-with-bears | MEDIA-OBSESSED-WITH-BEARS | MED         |
| Rudolf von Treppenwitz | 2         | Trouble for troubled troublemakers | 2                 | 30         | trouble-for-troubled      | TROUBLE-FOR-TROUBLED      | TRO         |
| Rudolf von Treppenwitz | 2         | Candidate is jerk, alleges rival   | 2                 | 26         | candidate-is-jerk         | CANDIDATE-IS-JERK         | CAN         |
| Anonymous Contributor  | 3         | Bad things gone, say good people   | 3                 | 23         | bad-things-gone           | BAD-THINGS-GONE           | BAD         |
| Markoff Chaney         | 4         | Balloon goons doomed               | 4                 | 24         | balloon-goons-doomed      | BALLOON-GOONS-DOOMED      | BAL         |

#### Materialized View - log_err_date

This materialized view creates a log error table that captures only error data from log table. Also the time column is log table is denoted as "time" type. This view will convert the time to date for easy representation in report.

```

create materialized view  log_err_date as
select time::timestamp::date as err_date, COUNT(1) AS total_logs,
SUM( CASE WHEN status !=  '200 OK' THEN 1 ELSE 0 END) AS not_ok_logs
from log GROUP BY err_date  ORDER BY err_date ASC;
```

##### Running the Select on log_err_date materialized view

err_date | total_logs | not_ok_logs
------------+------------+-------------
2016-07-01 | 38705 | 274
2016-07-02 | 55200 | 389
2016-07-03 | 54866 | 401
2016-07-04 | 54903 | 380
2016-07-05 | 54585 | 423
2016-07-06 | 54774 | 420
2016-07-07 | 54740 | 360
2016-07-08 | 55084 | 418
2016-07-09 | 55236 | 410
2016-07-10 | 54489 | 371
2016-07-11 | 54497 | 403
2016-07-12 | 54839 | 373
2016-07-13 | 55180 | 383
2016-07-14 | 55196 | 383
2016-07-15 | 54962 | 408
2016-07-16 | 54498 | 374
2016-07-17 | 55907 | 1265
2016-07-18 | 55589 | 374
2016-07-19 | 55341 | 433
2016-07-20 | 54557 | 383
2016-07-21 | 55241 | 418
2016-07-22 | 55206 | 406
2016-07-23 | 54894 | 373
2016-07-24 | 55100 | 431
2016-07-25 | 54613 | 391
2016-07-26 | 54378 | 396
2016-07-27 | 54489 | 367
2016-07-28 | 54797 | 393
2016-07-29 | 54951 | 382
2016-07-30 | 55073 | 397
2016-07-31 | 45845 | 329
(31 rows)

## SQL Analysis

- SQL for The most popular three articles of all time

```
select a.title as Title, l.count as views from author_articles a, log_count_status_path l
where a.slug_upper = l.slug_upper order by l.count desc limit 3;
```

- SQL for The most popular article authors of all time

```
select a.name as Author,  sum(l.count) as views from author_articles a, log_count_status_path l where a.slug_upper = l.slug_upper  group by a.name order by views desc;
```

- SQL for The days in which highest error rate occured

log err date is derived by selecting count(1) of records from log_err_date. This count will give only error records. The derived count divided by total error records from log table will give the percent of error records. This set is grouped by the date. Below SQL for better understanding.

```

select method, status, TO_CHAR(err_date :: DATE, 'Mon dd, yyyy'), count(1) count,
round(
CAST(count(1)\*100::float/(select count(1)::float from log) as numeric)
,2)||'% errors'
error_percent
from log_err_date
group by method, status, err_date
order by error_percent desc ;

```

## Installing

Run the articlereport.py in the target instance by using below command (assuming python3 is installed)

```shell
python articlereport.py
```

<i>Running the tests to generate report, run the articlereport.py program
</i>

- When the program is run it will generate below report (few lines printed from output)

```shell
vagrant@vagrant:/vagrant\$ python articlereport.py
```

###### The most popular three articles of all time

Candidate is jerk, alleges rival -- 338647 views <BR>
Bears love berries, alleges bear -- 253801 views <BR>
Bad things gone, say good people -- 170098 views <BR>

###### The most popular article authors of all time

Ursula La Multa -- 507594 views <BR>
Rudolf von Treppenwitz -- 423457 views <BR>
Anonymous Contributor -- 170098 views <BR>
Markoff Chaney -- 84557 views <BR>

###### Day on which highest rate of requests lead to error

Jul 17, 2016 -- 2.26% errors
Jul 24, 2016 -- 0.78% errors
Jul 19, 2016 -- 0.78% errors
Jul 05, 2016 -- 0.77% errors
Jul 06, 2016 -- 0.77% errors
Jul 21, 2016 -- 0.76% errors
Jul 08, 2016 -- 0.76% errors
Jul 15, 2016 -- 0.74% errors
Jul 11, 2016 -- 0.74% errors
Jul 09, 2016 -- 0.74% errors
Jul 22, 2016 -- 0.74% errors
Jul 03, 2016 -- 0.73% errors
Jul 26, 2016 -- 0.73% errors
Jul 28, 2016 -- 0.72% errors
Jul 30, 2016 -- 0.72% errors
Jul 25, 2016 -- 0.72% errors
Jul 31, 2016 -- 0.72% errors
Jul 01, 2016 -- 0.71% errors
Jul 29, 2016 -- 0.7% errors
Jul 02, 2016 -- 0.7% errors
Jul 20, 2016 -- 0.7% errors
Jul 04, 2016 -- 0.69% errors
Jul 14, 2016 -- 0.69% errors
Jul 16, 2016 -- 0.69% errors
Jul 13, 2016 -- 0.69% errors
Jul 10, 2016 -- 0.68% errors
Jul 23, 2016 -- 0.68% errors
Jul 12, 2016 -- 0.68% errors
Jul 18, 2016 -- 0.67% errors
Jul 27, 2016 -- 0.67% errors
Jul 07, 2016 -- 0.66% errors

## Test SQLs in postgresql DB news

connect to psqlgresql news DB

```
psql -d news
```

Run below sqls to verify data <BR>

- validate most popular three articles of all time

```
select a.title as Title, l.count ||' views' as views from
author_articles a, log_count_status_path l
where a.slug_upper = l.slug_upper order by l.count desc limit 3;
```

- verify The most popular article authors of all time

```
select a.name as Author, sum(l.count) as views from
author_articles a, log_count_status_path l
where a.slug_upper = l.slug_upper
group by a.name
order by views desc ;
```

```
select a.name, a.slug_upper, l.count from
author_articles a, log_count_status_path l
where a.slug_upper = l.slug_upper order by l.count desc ;
```

- validate log err date

```
select err_date, sum(not_ok_logs)
from log_err_date
group by err_date;
```

--sum of the above count gives - 12908

--get count(\*) of err data from log

```
select count(1) from log where status = '404 NOT FOUND';
```

--above counts gives - 12908

We work on the 12908 records against the whole set from log to get the highest error rate day

## Authors

- **Raji Ramakrishna** - \*Initial work for Project:Log Analysis\*\*

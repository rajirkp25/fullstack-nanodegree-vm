# #!/usr/bin/env python3
# Database code for the article analysis, full solution!

import psycopg2

DBNAME = "news"


def get_popular_articles():
    "Return the most popular three articles of all time"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sql = """SELECT a.title AS Title, l.count AS views
         FROM author_articles a, log_count_status_path l
         WHERE a.slug_upper = l.slug_upper
         ORDER BY l.count DESC LIMIT 3"""
    c.execute(sql)
    rows = c.fetchall()
    db.close()
    print('')
    print('The most popular three articles of all time')
    print('-------------------------------------------')
    for row in rows:
        article = row[0]
        count = int(row[1])
        print(article + ' -- ' + str(count) + ' views')


def get_popular_authors():
    "Return most popular article authors of all time"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sql = """SELECT a.name AS Author,
         SUM(l.count) AS views
        FROM author_articles a,
        log_count_status_path l
        WHERE a.slug_upper = l.slug_upper
        GROUP BY a.name
        ORDER BY views DESC """
    c.execute(sql)
    rows = c.fetchall()
    db.close()
    print('')
    print('The most popular article authors of all time')
    print('-------------------------------------------')

    for row in rows:
        author = row[0]
        count = int(row[1])
        print(author + ' -- ' + str(count) + ' views')


def get_err_days():
    "Return the day where highest rate of requests lead to error"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sql = "SELECT TO_CHAR(err_date :: DATE, 'Mon dd, yyyy'), \
            round(CAST((not_ok_logs/total_logs::float) AS numeric)*100, 2) \
            AS error_percent \
            FROM log_err_date \
            GROUP BY err_date, \
                    not_ok_logs, \
                    total_logs \
            ORDER BY error_percent DESC"

    c.execute(sql)
    rows = c.fetchall()
    print('')
    print('Day on which highest rate of requests lead to error')
    print('---------------------------------------------------------------')
    for row in rows:
        date = row[0]
        count = float(row[1])
        print(date + ' -- ' + str(count) + '%'' errors')


if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_err_days()
else:
    print('Importing ...')

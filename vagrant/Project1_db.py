import psycopg2


DBNAME = "news"


def part1():
    query1 = """SELECT articles.title, articles.slug, log.path,
                    count(log.path) as num
                        FROM articles JOIN log
                        ON log.path = CONCAT('/article/', articles.slug)
                        GROUP BY log.path, articles.slug, articles.title
                    ORDER BY num DESC
                    LIMIT 3;"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query1)
    part1 = c.fetchall()
    return part1


def part2():
    query2 = """SELECT totals.name, totals.totals
                FROM (SELECT authors.name, SUM(authors.totals) as totals
                        FROM (SELECT totalcounts.totals, authors.name,
                                authors.id, totalcounts.author
                                FROM (SELECT articles.title, articles.author,
                                articles.slug, log.path,
                                count(log.path) as totals
                        FROM articles JOIN log
                        ON log.path = CONCAT('/article/', articles.slug)
                        GROUP BY log.path, articles.slug, articles.title,
                                articles.author)
                                        as totalcounts
                                JOIN authors ON authors.id =
                                totalcounts.author)
                                as authors
                        GROUP BY authors.name) as totals
                        ORDER BY totals.totals DESC;"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query2)
    part2 = c.fetchall()
    return part2


def part3():
    query3 = """SELECT error.totaldate, error.average
                FROM (SELECT totalviews.totaldate, errors.errorsdate,
                (cast(errors.num as decimal) / totalviews.num) * 100
                as average
                        FROM (SELECT DATE(log.time) as totaldate,
                        count(log.time) as num
                                FROM log GROUP BY totaldate) as totalviews
                                JOIN (SELECT DATE(log.time) as errorsdate,
                                log.status, count(log.status) as num
                                FROM log WHERE log.status = '404 NOT FOUND'
                                GROUP BY errorsdate, log.status) as errors
                                ON totalviews.totaldate
                                = errors.errorsdate) as error
                WHERE error.average > 1;"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query3)
    part3 = c.fetchall()
    return part3

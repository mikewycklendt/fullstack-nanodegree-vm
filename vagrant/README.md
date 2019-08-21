# Project 1: Logs Analysis

## Description

This project analyzes the logs of a website to determine what the most popular articles on the website were, how nany views each author got for their articles and if any pages got errors on more than 1% of attempted page views.  It works off a database that has three tables, log, articles and authors.

In order to run this program you need to have a virtual machine installed.  I use vagrant and virtualbox which are free for download.  Once you have installed vagrant and virtualbox log into the server with vagrant ssh and then install the database.  The database can be found here:

```
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
```

Unzip the file into your working directory and cd into it onto the virtual machine and run:

```
psql -d news -f newsdata.sql
```

I chose to do this project with nested select statements.  I'll break down each SELECT in this readme.  I saved the python file as Project1.py in the .vagrant folder because when I tried to save it anywhere else I got a file not found error.  The project is made up of two files, Project1.py and Project1_db.py.  Project1.py creates the text file with the answers and Project1_db.py has three functions with a database query in each.

When I was trying to write the answers to a text file, \n wasn't giving me line breaks so I had to use \r\n to get the line breaks to show up.

## Part 1

I used two select statements in my query for part 1.  the innermost select statement is:

```
(SELECT articles.title, articles.slug, log.path, count(log.path) as num 
FROM articles JOIN log 
ON log.path LIKE CONCAT('%', articles.slug, '%') 
GROUP BY log.path, articles.slug, articles.title) as totals
```

That gave me the count of each path relative to the corresponding slug and article title.  

The outer select statement is

```
SELECT totals.title, SUM(num) as totals 
FROM (totals) 
GROUP BY totals.title 
ORDER BY totals DESC;
```

That added together all the varying paths with the same article title.

## Part 2

This one was a little more complicated.  I had to use five select statements.  I'll break them down starting with the innermost select.

```
(SELECT articles.title, articles.author, articles.slug, log.path, count(log.path) as num 
FROM articles JOIN log ON log.path LIKE CONCAT('%', articles.slug, '%') 
GROUP BY log.path, articles.slug, articles.title, articles.author) as counts
```

This is the same select as the innermost select from Part 1 with the added column of author id.

```
(SELECT counts.title, counts.author, SUM(counts.num) as totals 
FROM (counts) as counts 
GROUP BY counts.title, counts.author) as totalcounts
```
This is the same select as the outermost select from Part 1 with the added column of part 1.  It adds all the articles with varying paths together to give me a table with the number of article views for each article with the corresponding author id.

```
(SELECT totalcounts.totals, authors.name, authors.id, totalcounts.author 
FROM (totalcounts) as totalcounts 
JOIN authors ON authors.id = totalcounts.author) as authors
```
This joins the totalcounts select table with the authors table to give me a column with the author's name for each article and number of views that article had.

```
(SELECT authors.name, SUM(authors.totals) as totals 
FROM (authors) as authors 
GROUP BY authors.name) as totals 
```

This select adds together the article views of all the articles written by each author.

```
SELECT totals.name, totals.totals 
FROM (totals) as totals 
ORDER BY totals.totals DESC;
```

This select orders the table by the number of views each author had from most to least.  I would have liked to add the ORDER BY in the totals select statement but I kept getting an error.

## Part 3

For part three I used four select statements.  I'll go from innermost to outermost.

```
(SELECT DATE(log.time) as errorsdate, log.status, count(log.status) as num 
FROM log WHERE log.status = '404 NOT FOUND' 
GROUP BY errorsdate, log.status) as errors
```

This select groups the logs by their date and counts the number of times 404 NOT FOUND came up for each date.

```
SELECT DATE(log.time) as totaldate, count(log.time) as num 
FROM log GROUP BY totaldate) as totalviews 
JOIN (errors)
ON totalviews.totaldate = errors.errorsdate
```

This joins the table totalviews with the errors table to give me a column for the total number of views for each date and the number or errors for that date.

```
(SELECT totalviews.totaldate, errors.errorsdate, 
(cast(errors.num as decimal) / totalviews.num) * 100 as average 
FROM (totalviews)
JOIN (errors)
ON totalviews.totaldate = errors.errorsdate) as error
```

This creates a column that gives me a column with the average amounts of errors for each date.

```
SELECT error.totaldate, error.average 
FROM (error)
WHERE error.average > 1;
```

This filters the error table to only show dates where the average amount of errors is above 1%.
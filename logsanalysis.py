#!/usr/bin/env python

import psycopg2
import sys

DB_NAME = "news"


def connect(database_name):
    # Connects to the database :  "news"
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        # Execute queries and fetches results
        c = db.cursor()
        # Execute input query from cursor
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        # Then exit the program
        sys.exit(1)
        raise e


def fetch_results(query):
    db, c = connect(DB_NAME)
    c.execute(query)
    # fetch results from cursor
    results = c.fetchall()
    c.close()
    return results


def most_viewed():
    print("Q.1 What are the most popular three articles of all time?" + '\n')
    query1 = """
      SELECT article_view.title, article_view.view
      FROM article_view
      ORDER BY article_view.view DESC
      LIMIT 3;
    """
    most_viewed_results = fetch_results(query1)
    for line in most_viewed_results:
        print('"' + str(line[0]) + '"' + ' - ' + str(line[1]) + ' views')
    print('\n')


def most_popular_author():
    print("Q2. Who are the most popular article authors of all time?" + '\n')
    query2 = """
    SELECT article_view.name, SUM(article_view.view) AS author_view
    FROM article_view
    GROUP BY article_view.name
    ORDER BY author_view DESC;
    """
    most_popular_results = fetch_results(query2)
    for line in most_popular_results:
        print('"' + str(line[0]) + '"' + ' - ' + str(line[1]) + ' views')
    print('\n')


def most_error_day():
    q3 = """
        Q3. On which days did more than
        1% of requests lead to errors?
    """
    print(q3 + '\n')
    query3 = """
    SELECT *
    FROM error_rate
    WHERE error_rate.percentage > 1
    ORDER BY error_rate.percentage DESC;
    """
    error_results = fetch_results(query3)
    print(str(error_results[0][0]) + ' -- ' + str(error_results[0][1]) +
          ' errors')
    print('\n')


if __name__ == '__main__':
    most_viewed()
    most_popular_author()
    most_error_day()

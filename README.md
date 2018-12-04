# Log Analysis Project
This is a project for Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

## Project Description:
### About the logs analysis project
You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an **internal reporting tool** that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

#### Why this project?
In this project, you will stretch your SQL database skills. You will get practice interacting with a live database both from the command line and from your code. You will explore a large database with over a million rows. And you will build and refine complex queries and use them to draw business conclusions from data.

#### Report generation
Building an informative summary from logs is a real task that comes up very often in software engineering. For instance, at Udacity we collect logs to help us measure student progress and the success of our courses. The reporting tools we use to analyze those logs involve hundreds of lines of SQL.

#### Database as shared resource
In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.

This shows one of the valuable roles of a database server in a real-world application: it's a point where different pieces of software (a web app and a reporting tool, for instance) can share data.

![Just one of many queries Udacity uses for logs analysis](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57bf410d_pasted-image-at-2016-08-24-18-22/pasted-image-at-2016-08-24-18-22.png)

Just one of many queries Udacity uses for logs analysis.

## Your assignment: Build it!
Your task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the `psycopg2` module to connect to the database.

### So what are we reporting, anyway?
Here are the questions the reporting tool should answer. The example answers given aren't the right ones, though!

### Questions to Answer:
1. **What are the most popular three articles of all time?** Which articles have been 
accessed the most? Present this information as a sorted list with the most popular 
article at the top.

1. **Who are the most popular article authors of all time?** That is, when you sum up 
all of the articles each author has written, which authors get the most page views? 
Present this as a sorted list with the most popular author at the top.

1. **On which days did more than 1% of requests lead to errors?**  The log table 
includes a column status that indicates the HTTP status code that the news site sent 
to the user's browser. 

## This Project Requires a Bit of Setup:
This project is run in a virutal machine created using Vagrant so there are a few steps
to get set up:
#### Installing the dependencies and setting up the files:
1. Install [Vagrant](https://www.vagrantup.com/)
1. Install [VirtualBox](https://www.virtualbox.org/)
1. Download the vagrant setup files from [Udacity's Github](https://github.com/udacity/fullstack-nanodegree-vm)
These files configure the virtual machine and install all the tools needed to run this project.
1. Download the database setup: [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
1. Unzip the data to get the newsdata.sql file.
1. Put the newsdata.sql file into the vagrant directory
1. Download this project: [log analysis](https://github.com/nileshlande12/UD-LogsAnalysis-FullStack-WebDeveloper-Nanodegree-Program)
1. Upzip as needed and copy all files into the vagrant directory into a folder called UD-LogsAnalysis-FullStack-WebDeveloper-Nanodegree-Program

#### Start the Virtual Machine:
1. Open Terminal and navigate to the project folders we setup above.
1. cd into the vagrant directory
1. Run ``` vagrant up ``` to build the VM for the first time.
1. Once it is built, run ``` vagrant ssh ``` to connect.
1. cd into the correct project directory: ``` cd /vagrant/UD-LogsAnalysis-FullStack-WebDeveloper-Nanodegree-Program ```

#### Load the data into the database:
1. Load the data using the following command: ``` psql -d news -f newsdata.sql ```
1. *Note:* Checkout Udacity's [FAQ](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91) 
page if you are running into any errors here.

3. Create Views
```sql
CREATE VIEW author_info AS
SELECT authors.name, articles.title, articles.slug
FROM articles, authors
WHERE articles.author = authors.id
ORDER BY authors.name;
```

```sql
CREATE VIEW path_view AS
SELECT path, COUNT(*) AS view
FROM log
GROUP BY path
ORDER BY path;
```

```sql
CREATE VIEW article_view AS
SELECT author_info.name, author_info.title, path_view.view
FROM author_info, path_view
WHERE path_view.path = CONCAT('/article/', author_info.slug)
ORDER BY author_info.name;
```

```sql
CREATE VIEW total_view AS
SELECT date(time), COUNT(*) AS views
FROM log 
GROUP BY date(time)
ORDER BY date(time);
```

```sql
CREATE VIEW error_view AS
SELECT date(time), COUNT(*) AS errors
FROM log WHERE status = '404 NOT FOUND' 
GROUP BY date(time) 
ORDER BY date(time);
```

```sql
CREATE VIEW error_rate AS
SELECT total_view.date, (100.0*error_view.errors/total_view.views) AS percentage
FROM total_view, error_view
WHERE total_view.date = error_view.date
ORDER BY total_view.date;
```

## Run The Project Already!
1. You should already have vagrant up and be connected to it. 
1. If you aren't already, cd into the correct project directory: ``` cd /vagrant/UD-LogsAnalysis-FullStack-WebDeveloper-Nanodegree-Program ```
1. Run ``` python loganalysis.py ```

Generating this information will take several seconds, but will now start loading. 

## Expected Output: 
    Calculating Results...
    TOP THREE ARTICLES BY PAGE VIEWS:
        (1) "Candidate is jerk, alleges rival" with 338647 views
        (2) "Bears love berries, alleges bear" with 253801 views
        (3) "Bad things gone, say good people" with 170098 views
    TOP THREE AUTHORS BY VIEWS:
        (1) Ursula La Multa with 507594 views
        (2) Rudolf von Treppenwitz with 423457 views
        (3) Anonymous Contributor with 170098 views
    DAYS WITH MORE THAN 1% ERRORS:
        July 17, 2016 -- 2.26% errors

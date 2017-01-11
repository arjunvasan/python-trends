Pytrends
======

A python module for grabbing data from Google Trends & Google Correlate (coming soon)

Google Trends
-------------
To download data from Google Trends:

    import google
    trends = google.Trends(google.Session("username", "password"))

    // get trends data from 2004 onwards
    data = trends.fetch(q="Trump")

    // get data for 24 months starting 10/2014
    data = trends.fetch(q="Trump", date="10/2014 24m")

    // get data for last 24 hours
    data = trends.fetch(q="Trump", date="now 24-H")

    // get data for multiple search terms
    data = trends.fetch(q="Trump,Clinton,Obama")
    (returns three columns for 'trump','clinton' and 'obama')

    // query by google property ('news','youtube','shopping','web' (default))
    data = trends.fetch(q="Trump,Clinton,Obama",gprop='news')

    // limit query to geographical region
    data = trends.fetch(q="Trump,Clinton,Obama",geo='US-CA')
    (trends for California only)
    
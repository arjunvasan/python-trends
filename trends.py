# -*- coding: utf-8 -*-
"""
:Author: `<arjun.vasan@gmail.com>`_
"""

import urllib
from datetime import datetime
import json
import numpy as np
from copy import copy
from StringIO import StringIO
import pandas as pd
from web import extract, find_html_elements, search_html
from nltk import clean_html

class Trends(object):
    def __init__(self, google_login):

        super(Trends, self).__init__()

        self.http_access = google_login
        self.get = self.http_access.get
        self.post = self.http_access.post

        self.url = 'http://www.google.com/trends/trendsReport'

    def build_trends_request(self, **kwargs):
        """
        Parameters:
        q (string or array) - The search term(s) to return (separated by comma if string).
        geo (string or array) - The (2-character) country or countries from which users are
            searching for the search terms.
        date (string or datetime) - use google trends format (today 12-m, now 12-H, 10/2012 12m etc)
        gprop (string) - "news", "youtube", "shopping" etc (defaults to web search)
        """

        params = {
            'export': 1,
            'hl': 'en-US',
            'geo': 'us'
        }

        params.update(kwargs)

        # Prepare inputs
        # query and country can be either an array or a csv string
        if type(params['q']) is str or type(params['q']) is unicode:
            params['q'] = params['q'].split(',')

        if type(params['geo']) is str or type(params['geo']) is unicode:
            params['geo'] = params['geo'].split(',')


        # Convert the date field if provided as a datetime object
        if "date" in params and type(params["date"]) is datetime:
            params["date"] = params["date"].strftime("%Y-%m-%dT%H\:%M\:%S 24H")


        if len(params['geo']) > 1:
            params['cmpt'] = 'geo'
        else:
            params['cmpt'] = 'q'

        if len(params['q']) > 0:
            params['q'] = ','.join(params['q'])

        if len(params['geo']) > 0:
            params['geo'] = ','.join(params['geo'])

        print self.url + "?" + urllib.urlencode(params)

        return self.url, params


    def fetch_trends_csv(self, usebrowser=False, browser_timeout=60, display=False, **kwargs):
        """
        Fetch CSV from Google Trends
        """

        url, params = self.build_trends_request(**kwargs)

        if display:
            print url
            print params
            print url + "?" + urllib.urlencode(params)

        data = self.get(self.url, params=params).text

        if '<!DOCTYPE html><html ><head>' in data:
            raise Exception('Google did not return a csv file\n\n' + clean_html(data))

        return data

    @staticmethod
    def _from_csv(data):
        trend_data = extract(data, r'Interest over time(.*?)(\n\n\n)')
        df = pd.read_csv(StringIO(trend_data), delimiter=',')
        # Convert all the search trends to float
        for search_term in df.columns[1:]:

            is_percent = (type(df[search_term][0]) is str) and df[search_term][0].endswith('%')

            if is_percent:
                for i in range(len(df)):
                    if df[search_term][i].strip(' ') == '':
                        df[search_term][i] = np.nan
                    else:
                        df[search_term][i] = float(df[search_term][i].strip('%'))/100.0

            df[search_term] = df[search_term].convert_objects(convert_numeric=True)

        # Split the week field into start and end
        if "Week" in df.columns:
            start = [item.split(' - ')[0] for item in df['Week']]
            end = [item.split(' - ')[1] for item in df['Week']]
            df['start'] = start
            df['end'] = end
            del df['Week']

            df.start = pd.to_datetime(df.start)
            df.end = pd.to_datetime(df.end)


        def str_2_datetime(s):
            if "UTC" in s:
                return datetime.strptime(t, "%Y-%m-%d-%H:%M UTC")
            else:
                return datetime.strptime(t, "%Y-%m-%d-%H:%M")

        # Convert the time field
        if "Time" in df.columns:
            dates = [str_2_datetime(t) for t in df.Time]
            df["Time"] = dates

        return df


    def entity_query(self, name):
        result = self.get('http://www.google.com/trends/entitiesQuery', params={
            "q": name,
            "tn": 4
        })
        data = json.loads(result.text)["entityList"]
        return data


    def fetch(self, compare=True, usebrowser=False, **kwargs):
        return self._from_csv(
            self.fetch_trends_csv(
                usebrowser=usebrowser, 
                **kwargs
            )
        )

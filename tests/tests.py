import pandas as pd
import google
import unittest

"""
Test google account
email: nasavjunra@gmail.com
password: ZAQ!@WSX
"""

SESSION = None

class TestSuite(unittest.TestCase):
    def get_session(self):
        global SESSION
        if SESSION is None:
            SESSION = google.Session("nasavjunra@gmail.com", "ZAQ!@WSX")
        return SESSION

    def test_get_session(self):
        assert isinstance(self.get_session(), google.Session)

    def test_google_login(self):
        self.get_session()

    def test_trends_fetch(self):

        session = self.get_session()
        trends = google.Trends(session)
        data = trends.fetch(q="Trump")

        assert isinstance(data, pd.DataFrame)
        assert len(data) > 500

if __name__ == '__main__':
    unittest.main()



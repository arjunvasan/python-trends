# -*- coding: utf-8 -*-
"""
:Author: `<arjun.vasan@gmail.com>`_
"""


class ExceededQuotaException(Exception):
    """
    Exception for when Google returns the message "You have exceeded your
    quota."
    """
    pass

def handle_HTTPError(error):

    data = {
        'code': error.code,
        'url': error.geturl(),
        'reason': error.reason,
    }

    message = """HTTP Error %(code)d
    URL: %(url)s
    Reason: %(reason)s""" % data

    error.message = message

    print message
    raise error

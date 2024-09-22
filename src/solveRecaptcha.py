import sys
import os
from twocaptcha import TwoCaptcha


def solveRecaptcha(sitekey, url):

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    api_key = "dbabcc2df0eb91a8a022988d96dfbe06"
    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey= sitekey,
            url=url)

    except Exception as e:
        print(e)

    else:
        return result
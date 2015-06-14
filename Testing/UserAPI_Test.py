__author__ = 'etye'
import unittest
import requests
from Testing.config import __CONFIG__

class UserTestPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        debug = __CONFIG__['DEBUG']
        if debug:
            url = __CONFIG__['PATHS']['DEBUG']
        else:
            url = __CONFIG__['PATHS']['PRODUCTION']
        cls.url_ = url
        request = requests.get(url+'api/qa/init')
        if 200 <= request.status_code <= 299:
            print 'Initialized'

    def test_getUserByToken_invalid(self):
        r = requests.get(self.__class__.url_+'api/getUserByToken/invalidtoken')
        self.assertEquals(r.status_code, 403)


    def test_getUserByToken_valid(self):
        r = requests.get(self.__class__.url_+'api/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['username'], 'qa_student')


    def test_getUserByToken_empty(self):
         r = requests.get(self.__class__.url_+'api/getUserByToken/')
         self.assertEquals(r.status_code, 400)



if __name__ == '__main__':
    unittest.main()
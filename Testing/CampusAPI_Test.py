__author__ = 'etye'
import unittest
import requests
from Testing.config import __CONFIG__
class CampusTestPlan(unittest.TestCase):
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

    def test_campusesGet_invalidToken(self):
            r = requests.get(self.__class__.url_+'api/campuses/getAll/invalidtoken')
            self.assertEquals(r.status_code, 403)

    def test_campusesGet_validToken_testArraySize(self):
            r = requests.get(self.__class__.url_+'api/campuses/getAll/'+__CONFIG__['TOKENS']['STUDENT'])
            self.assertEquals(r.status_code, 200)
            self.assertTrue(len(r.json())>= 1)

    def test_campusCreate_Lecturer(self):
            payload = {'title': 'Campus name', 'email_ending': '@campus.ac.com','avatar_url': 'http://location.domain.com/image.jpg'}
            r = requests.post(self.__class__.url_+'api/campuses/create/'+__CONFIG__['TOKENS']['LECTURER'],data=payload)
            self.assertEquals(r.status_code, 201)

    def test_campusCreate_Student(self):
            payload = {'title': 'Campus name', 'email_ending': '@campus.ac.com','avatar_url': 'http://location.domain.com/image.jpg'}
            r = requests.post(self.__class__.url_+'api/campuses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
            self.assertEquals(r.status_code, 403)

    def test_campusCreate_InvalidToken(self):
            payload = {'title': 'Campus name', 'email_ending': '@campus.ac.com','avatar_url': 'http://location.domain.com/image.jpg'}
            r = requests.post(self.__class__.url_+'api/campuses/create/invalidToken',data=payload)
            self.assertEquals(r.status_code, 403)

if __name__ == '__main__':
    unittest.main()
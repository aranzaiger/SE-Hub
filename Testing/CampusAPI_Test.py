__author__ = 'etye'
import unittest
import requests
import json
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

    #/api/campuses/create/<string:token>
    def test_campusCreate_lecturer(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/campuses/create/'+__CONFIG__['TOKENS']['LECTURER']
        data = {
            'title': 'Campus name',
            'email_ending': '@campus.ac.com',
            'avatar_url': 'http://location.domain.com/image.jpg'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 201)

    def test_campusCreate_student(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/campuses/create/'+__CONFIG__['TOKENS']['STUDENT']
        data = {
            'title': 'Campus name',
            'email_ending': '@campus.ac.com',
            'avatar_url': 'http://location.domain.com/image.jpg'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)
        self.assertEquals(r._content, '{"message": "Invalid token or not a lecturer!"}')

    def test_campusCreate_invalidToken(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/campuses/create/invalidToken'
        data = {
            'title': 'Campus name',
            'email_ending': '@campus.ac.com',
            'avatar_url': 'http://location.domain.com/image.jpg'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)
        self.assertEquals(r._content, '{"message": "Invalid token or not a lecturer!"}')

    def test_campusesGet_invalidToken(self):
        r = requests.get(self.__class__.url_+'api/campuses/getAll/invalidtoken')
        self.assertEquals(r.status_code, 403)

    def test_campusesGet_validToken_testArraySize(self):
        r = requests.get(self.__class__.url_+'api/campuses/getAll/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.json())>= 1)

    def test_campusesGet_validToken_testArraySize(self):
        r = requests.get(self.__class__.url_+'api/campuses/getAll/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.json())>= 1)




if __name__ == '__main__':
    unittest.main()
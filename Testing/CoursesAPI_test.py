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

    def test_courseCreate_lecturer(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['LECTURER']
        data = {
            'courseName': 'matan',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 201)

    def test_courseCreate_lecturerExsistingCourse(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['LECTURER']
        data = {
            'courseName': 'matan',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)

    def test_courseCreate_student(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT']
        data = {
            'courseName': 'matan',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)

    def test_courseCreate_invalidToken(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/courses/create/invalidToken'
        data = {
            'courseName': 'matan',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)

    def test_courseCreate_hebrewToken(self):
        #url = "http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER"
        url=self.__class__.url_+'api/courses/create/????'
        data = {
            'courseName': 'matan',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 404)

    #/api/courses/getCourseByCampusName/<string:name>
    def test_getCourseByCampusName_EXSISTING_CAMPUS(self):
        url=self.__class__.url_+'api/courses/getCourseByCampusName/'+__CONFIG__['CAMPUS_NAME']['JCE']
        r = requests.get(url)
        self.assertEquals(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
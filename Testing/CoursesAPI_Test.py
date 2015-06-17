__author__ = 'etye'
import unittest
import requests
import json
from Testing.config import __CONFIG__
class CoursesTestPlan(unittest.TestCase):
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

    def test_coursesCreate_Lecturer(self):
        headers = {'content-type': 'application/json'}
        url = 'http://se-hub.appspot.com/api/courses/create/_QA_TOKEN_TEST_LECTURER'
        params = {'seToken': 'seToken' }
        data = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }

        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        '''
        payload = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        '''
        # r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['LECTURER'],data=payload)
        #r = requests.post('http://localhost:8080/api/courses/create/_QA_TOKEN_TEST_LECTURER',data=payload)
        #self.assertEquals(r.status_code, 201)

    def test_coursesCreate_InvalidToken(self):
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/create/invalidToken'
        data = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        params = {'seToken': 'seToken' }
        r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)
        '''
        payload = {'courseName': 'Advance Math', 'campusName': 'JCE', 'startDate':'2015-14-3','endDate': '2015-29-6','taskFlag': 'False'}
        payload = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        r = requests.post(self.__class__.url_+'api/courses/create/invalidToken',data=payload)
        '''
    def test_coursesCreate_Student(self):
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/create/_QA_TOKEN_TEST_STUDENT'
        params = {'seToken': 'seToken' }
        data = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }

        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403, 'message: ' + r.json()['message'])

    def test_getCourseByCampusName(self):
        r = requests.get(self.__class__.url_+'api/courses/getCourseByCampusName/'+__CONFIG__['TOKENS']['CAMPUS_NAME'])
        self.assertEquals(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
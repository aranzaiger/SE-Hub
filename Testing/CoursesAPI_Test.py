__author__ = 'etye'
import unittest
import requests
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
        payload = {'courseName': 'Advance Math', 'campusName': 'JCE', 'startDate':'2015-14-3','endDate': '2015-29-6','taskFlag': 'False'}
        r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['LECTURER'],data=payload)
        self.assertEquals(r.status_code, 201)

    def test_coursesCreate_InvalidToken(self):
        payload = {'courseName': 'Advance Math', 'campusName': 'JCE', 'startDate':'2015-14-3','endDate': '2015-29-6','taskFlag': 'False'}
        r = requests.post(self.__class__.url_+'api/courses/create/invalidToken',data=payload)
        self.assertEquals(r.status_code, 403)

    def test_coursesCreate_Student(self):
        payload = {'courseName': 'Advance Math', 'campusName': 'JCE', 'startDate':'2015-14-3','endDate': '2015-29-6','taskFlag': 'False'}
        r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        self.assertEquals(r.status_code, 403)

    def test_getCourseByCampusName(self):
        r = requests.get(self.__class__.url_+'api/courses/getCourseByCampusName/'+__CONFIG__['TOKENS']['CAMPUS_NAME'])
        self.assertEquals(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
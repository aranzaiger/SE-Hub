__author__ = 'etye'
import unittest
import requests
import json
import datetime
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
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_ +'api/courses/create/_QA_TOKEN_TEST_LECTURER'
        #params = {'seToken': 'seToken' }
        data = {
            'courseName': 'Advance Math',
            'campusName': 'JCE',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016, 'month' : 5, 'day' : 14}
        }

        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, data=json.dumps(data), headers=headers)
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
        print(r._content)
        if(r.status_code!=201):print("_____"+self._testMethodName+" has Failed"+"_____" + r._content)
        self.assertEquals(r.status_code, 201)


    def test_coursesCreate_InvalidToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/create/invalidToken'
        data = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_coursesCreate_Student(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/create/_QA_TOKEN_TEST_STUDENT'
        #params = {'seToken': 'seToken' }
        data = {
            'courseName': 'QA COURSE',
            'campusName': 'https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg',
            'projects': '@gay.lord.ultima.multi.omega',
            'startDate': {'year': 2015, 'month' : 4, 'day' : 3},
            'endDate': {'year': 2016,'month' : 6,'day' : 6}
        }

        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403, 'message: ' + r.json()['message'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_getCourseByCampusName(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/courses/getCourseByCampusName/JCE')
        self.assertEquals(r.status_code, 200)
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    #/api/courses/createMessage/<string:token>
    '''
    Payload
    - JSON Object, Example:
    {
    'courseName': 'Advance Math',
    'message': 'The lecture today is canceled'
    }
    '''
    def test_createMessage_lecturerToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/createMessage/_QA_TOKEN_TEST_LECTURER'
        #params = {'seToken': 'seToken' }
        data = {
            'courseName': 'Advance Math',
            'message': 'The lecture today is canceled'
        }

        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 201, 'message: ' + r.json()['message'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_createMessage_studentToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/createMessage/_QA_TOKEN_TEST_STUDENT'
        #params = {'seToken': 'seToken' }
        data = {
            'courseName': 'Advance Math',
            'message': 'The lecture today is canceled'
        }
        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403, 'message: ' + r.json()['message'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_createMessage_invalidToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/courses/createMessage/invalidToken'
        #params = {'seToken': 'seToken' }
        data = {
            'courseName': 'Advance Math',
            'message': 'The lecture today is canceled'
        }
        #r = requests.post(self.__class__.url_+'api/courses/create/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403, 'message: ' + r.json()['message'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

if __name__ == '__main__':
    unittest.main()
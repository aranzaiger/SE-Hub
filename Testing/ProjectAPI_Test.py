__author__ = 'etye'
import unittest
import requests
import json
#import logging
import datetime

from Testing.config import __CONFIG__
class ProjectTestPlan(unittest.TestCase):
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

    #/api/projects/create/<string:token>
    def test_projectCreate_lecturerToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/projects/create/'+__CONFIG__['TOKENS']['LECTURER']
        data = {
            'projectName': 'Advance Math',
            'courseName': 'JCE',
            'logo_url': 'http://location.domain.com/image.jpg',
            'gitRepository': 'http://location.git.com/somthing'
        }

        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 201)
        print("***********************************************")
        print(self._testMethodName+"Has finished")
        #print("Test Project Create w/ Lecturer token has finished")
        print("***********************************************")


    def test_projectCreate_studentToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/projects/create/'+__CONFIG__['TOKENS']['STUDENT']
        data = {
            'projectName': 'Advance Math',
            'courseName': 'JCE',
            'logo_url': 'http://location.domain.com/image.jpg',
            'gitRepository': 'http://location.git.com/somthing'
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 403)
        print("***********************************************")
        print(self._testMethodName+"Has finished")
        #print("Test Project Create w/ Lecturer token has finished")
        print("***********************************************")

    #/api/projects/deleteProject/<string:token>/<string:projectid>
    def test_projectDelete_studentToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/projects/create/'+__CONFIG__['TOKENS']['STUDENT']
        r = requests.delete(url)
        self.assertEquals(r.status_code, 403)
        print("***********************************************")
        print(self._testMethodName+"Has finished")
        #print("Test Project Create w/ Lecturer token has finished")
        print("***********************************************")

    def test_projectDelete_lecturerToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/projects/create/'+__CONFIG__['TOKENS']['STUDENT']
        r = requests.delete(url)
        self.assertEquals(r.status_code, 403)
        print("***********************************************")
        print(self._testMethodName+"Has finished")
        #print("Test Project Create w/ Lecturer token has finished")
        print("***********************************************")

    def test_projectDelete_invalidToken(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        headers = {'content-type': 'application/json'}
        url = self.__class__.url_+'api/projects/create/'+__CONFIG__['TOKENS']['STUDENT']
        r = requests.delete(url)
        self.assertEquals(r.status_code, 403)
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        #print("Test Project Create w/ Lecturer token has finished")
        print("***********************************************")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ProjectTestPlan)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()

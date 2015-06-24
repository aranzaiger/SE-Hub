__author__ = 'etye'
import unittest
import requests
import json
import datetime
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
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/invalidtoken')
        self.assertEquals(r.status_code, 204)
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_getUserByToken_valid(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['username'], 'qa_student')
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_getUserByToken_empty(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/')
        self.assertEquals(r.status_code, 204)
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_isStudent_Student(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertFalse(r.json()['isLecturer'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_isLecturer_Lecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isLecturer'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def  test_isFirstLogin_Student(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isFirstLogin'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_isFirstLogin_Lecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isFirstLogin'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_isClassIdListEmpty_Student(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['classes_id_list'],[])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_campuses_id_list_Student(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['campuses_id_list'],[])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_Student_isLecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertFalse(r.json()['isLecturer'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_Lecturer_isLecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isLecturer'])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_isClassIdListEmpty_Lecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['classes_id_list'],[])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_campuses_id_list_Lecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['campuses_id_list'],[])
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    #/api/users/updateUser/<string:token>

    def test_updateUser_lecturer(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        url=self.__class__.url_+'api/users/updateUser/'+__CONFIG__['TOKENS']['LECTURER']
        data = {
            'name': 'new name',
            'isLecturer': True,
            'campusName': 'JCE'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r._content, '{"message": "User updated"}')
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_updateUser_student(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        url=self.__class__.url_+'api/users/updateUser/'+__CONFIG__['TOKENS']['STUDENT']
        data = {
            'name': 'new name',
            'isLecturer': True,
            'campusName': 'JCE'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r._content, '{"message": "User updated"}')
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_updateUser_INVALID_TOKEN(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        url=self.__class__.url_+'api/users/updateUser/invalidToken'
        data = {
            'name': 'new name',
            'isLecturer': True,
            'campusName': 'JCE'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 400)
        self.assertEquals(r._content, '{"message": "Not a user!"}')
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

    def test_updateUser_HEBREW_TOKEN(self):
        print (datetime.datetime.now().time())
        print("***********************************************")
        print(self._testMethodName+"Has begun")
        print("***********************************************")
        url=self.__class__.url_+'api/users/updateUser/?????'
        data = {
            'name': 'new name',
            'isLecturer': True,
            'campusName': 'JCE'
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        self.assertEquals(r.status_code, 404)
        print("***********************************************")
        print(self._testMethodName+"Has finished Successfully")
        print("***********************************************")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UserTestPlan)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
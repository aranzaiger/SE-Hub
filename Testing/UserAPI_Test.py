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

    def test_getUserByToken_invalid(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/invalidtoken')
        self.assertEquals(r.status_code, 204)

    def test_getUserByToken_valid(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['username'], 'qa_student')

    def test_getUserByToken_empty(self):
         r = requests.get(self.__class__.url_+'api/users/getUserByToken/')
         self.assertEquals(r.status_code, 204)

    def test_isStudent_Student(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertFalse(r.json()['isLecturer'])

    def test_isLecturer_Lecturer(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isLecturer'])

    def  test_isFirstLogin_Student(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isFirstLogin'])

    def test_isFirstLogin_Lecturer(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isFirstLogin'])

    def test_isClassIdListEmpty_Student(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['classes_id_list'],[])

    def test_campuses_id_list_Student(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['campuses_id_list'],[])

    def test_Student_isLecturer(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['STUDENT'])
        self.assertEquals(r.status_code, 200)
        self.assertFalse(r.json()['isLecturer'])

    def test_Lecturer_isLecturer(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.json()['isLecturer'])

    def test_isClassIdListEmpty_Lecturer(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['classes_id_list'],[])

    def test_campuses_id_list_Lecturer(self):
        r = requests.get(self.__class__.url_+'api/users/getUserByToken/'+__CONFIG__['TOKENS']['LECTURER'])
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.json()['campuses_id_list'],[])

    def test_userUpdate_Student(self):
        payload = {'name': 'New Name', 'isLecturer': 'false'}
        r = requests.post(self.__class__.url_+'api/users/userUpdate/'+__CONFIG__['TOKENS']['STUDENT'],data=payload)
        self.assertEquals(r.status_code, 200)
        #data = {}
        #data['name'] = 'New Name'
        #data['isLecturer'] = 'false'
        #json_data = json.dumps(data)
        #r = requests.post(self.__class__.url_+'api/users/userUpdate/'+__CONFIG__['TOKENS']['STUDENT'],json_data)
        #self.assertEquals(r.status_code, 200)
        #self.assertEquals(r.json()['message'],'User updated')

if __name__ == '__main__':
    unittest.main()
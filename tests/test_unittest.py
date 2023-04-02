from app import app, mydb
from unittest import TestCase
import uuid


class AppTest(TestCase): 
    def test_signup(self):
        # generate unique id for test user
        username = "gh3ifmsdy"
        usermail = username + "@gmail.com"

        # test1 = good
        response = app.test_client().post("/signup", data={
                    "usermail": usermail, 
                    "name": username, 
                    "pass1": "Passw0rd!", 
                    "pass2": "Passw0rd!",
                    })
        
        self.assertEqual(response.status_code, 302)
        '''
        # test2 = mismatch passwords
        response = app.test_client().post("/signup", data={
                    "usermail": usermail, 
                    "name": username, 
                    "pass1": "Passw0rd!", 
                    "pass2": "Different!",
                    }, follow_redirects=True)

        # test3 = improper email
        response = app.test_client().post("/signup", data={
                    "usermail": username, 
                    "name": username, 
                    "pass1": "Passw0rd!", 
                    "pass2": "Passw0rd!",
                    }, follow_redirects=True)'''
        
        mysqlcursor = mydb.cursor(buffered=True)
        query = f"DELETE FROM Users WHERE `username`='{username}'"
        mysqlcursor.execute(query)
        mydb.commit()


    def test_editpost(self): 
        postid = str(uuid.uuid4())

        # connect to db and create post before editing
        mysqlcursor = mydb.cursor(buffered=True)
        addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
        addvals = (postid, 'testtitle', 'test_desc', 'bunny.jpg', 'sample', 0, 0)
        
        mysqlcursor.execute(addcom, addvals)
        mydb.commit()
        mysqlcursor.close()


        # test1 = good
        response = app.test_client().post('/edit/1', data={
                    "title": "test_title", 
                    "description": "test_description",
                })
        
        
        self.assertEqual(response.status_code, 302)
        

        mysqlcursor = mydb.cursor(buffered=True)
        
        query = f"DELETE FROM Posts WHERE `id`='{postid}'"
        mysqlcursor.execute(query)
        mydb.commit()

apptest =  AppTest()

apptest.test_signup()
apptest.test_editpost()
from app import app, mydb
import uuid

def test_comment():
    

    #create test user
    testusername="testing"
    testuser = str(uuid.uuid4())
    mysqlcursor = mydb.cursor(buffered=True)
    add_user = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals_user = ('test3', 'test@test.com', 'password', 'bio', 'default_profilepic.jpg', '0')
    mysqlcursor.execute(add_user, addvals_user)
    mydb.commit()

    #login test user
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = 'test3'

    #user is logged in
    response = client.get('/profile')
    assert response.status_code == 200

    
    #create post to test comment
    postid = str(uuid.uuid4())
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = (postid, 'unittest', 'unittest_desc', 'bunny.jpg', 'testusername', 0, 0)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    #load comments page for test post
    response = client.get('/comments/' + postid)
    assert response.status_code == 200

    #leave comment
    uniquecomment=str(uuid.uuid4())
    response = client.post('/comments/' + postid, data=dict(comment=uniquecomment), follow_redirects=True)
    assert response.status_code == 200

    #check comment is in database
    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(f"SELECT comment FROM Comments WHERE comment='{uniquecomment}'")
    checking = str(mysqlcursor.fetchall())
    assert uniquecomment in checking

    #load create post page
    response = client.get('/createpost')
    assert response.status_code == 200
    

    #create new post
    #data = {'title':'title', 'description':'description'}
    #response = client.post('/createpost', data=data, follow_redirects=True)
    #assert response.status_code == 200

    #response = app.test_client().post("/createpost", data={
    #            "title": "title", 
    #            "description": "desc", 
    #            "imagefile": "bunny.jpg", 
    #            }, follow_redirects=True)
    #assert response.status_code == 200
   
    

    #delete user
    mysqlcursor = mydb.cursor(buffered=True)
    del_user = f"DELETE FROM Users WHERE username='{'test3'}'"
    mysqlcursor.execute(del_user)
    mydb.commit()
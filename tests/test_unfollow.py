from app import app, mydb
import uuid

def test_unfollow():
    # create two users
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())

    # generic account info
    mysqlcursor = mydb.cursor(buffered=True)
    add_user1 = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals_user1 = ('user1', 'user1@test.com', 'password', 'user1 bio', 'user1 profile pic path', '0')
    add_user2 = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s)"
    addvals_user2 = ('user2', 'user2@test.com', 'password', 'user2 bio', 'user2 profile pic path', '0')

    mysqlcursor.execute(add_user1, addvals_user1)
    mysqlcursor.execute(add_user2, addvals_user2)
    mydb.commit()

    # login as user1
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user'] = 'user1'

    # follow user2 as user1
    response = client.post('/follow', data=dict(username='user2'), follow_redirects=True)
    assert response.status_code == 200

    # unfollow user2 as user1
    response = client.post('/unfollow', data=dict(username='user2'), follow_redirects=True)
    assert response.status_code == 200

    # check if user1 is not following user2
    mysqlcursor.execute(f"SELECT * FROM Follows WHERE follower='user1' AND following='user2'")
    result = mysqlcursor.fetchone()
    assert result is None

    # remove the 2 users
    query_user1 = f"DELETE FROM Users WHERE username='{'user1'}'"
    query_user2 = f"DELETE FROM Users WHERE username='{'user2'}'"
    mysqlcursor.execute(query_user1)
    mysqlcursor.execute(query_user2)
    mydb.commit()

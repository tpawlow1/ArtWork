import unittest
from app import app, mydb

class TestRecommendedPage(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.username = "testuser"
        self.following_username = "followinguser"

        # Create a test user and a user they are following
        mysqlcursor = mydb.cursor(buffered=True)
        mysqlcursor.execute(f"INSERT INTO Users (username, email, password) VALUES ('{self.username}', '{self.username}@example.com', 'testpassword')")
        mysqlcursor.execute(f"INSERT INTO Users (username, email, password) VALUES ('{self.following_username}', '{self.following_username}@example.com', 'testpassword')")
        mysqlcursor.execute(f"INSERT INTO Follows (follower, following) VALUES ('{self.username}', '{self.following_username}')")
        mysqlcursor.execute(f"INSERT INTO Posts (id, title, description, filepath, user, likes, dislikes) VALUES ('post1', 'Test post', 'This is a test post', '/path/to/file', '{self.following_username}', 0, 0)")
        mydb.commit()
        mysqlcursor.close()

    def tearDown(self):
        # Delete the test users and posts
        mysqlcursor = mydb.cursor(buffered=True)
        mysqlcursor.execute(f"DELETE FROM Posts WHERE user = '{self.following_username}'")
        mysqlcursor.execute(f"DELETE FROM Follows WHERE follower = '{self.username}'")
        mysqlcursor.execute(f"DELETE FROM Users WHERE username = '{self.following_username}'")
        mysqlcursor.execute(f"DELETE FROM Users WHERE username = '{self.username}'")
        mydb.commit()
        mysqlcursor.close()

    def test_get_following_posts(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['user'] = self.username

            response = client.get('/recommendedpage')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test post', response.data)

if __name__ == '__main__':
    unittest.main()


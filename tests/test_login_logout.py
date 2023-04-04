from app import app

def test_login():

    #Preconditions: The user has signed up and has been added to the database but isn't logged in.

    # test login with correct credentials
    login_response = app.test_client().post("/login", data={
        "username": "paulthottappilly",
        "password": "password",
    }, follow_redirects=True)

    assert login_response.status_code == 200
    assert "paulthottappilly" in login_response.data.decode('utf-8')

    # test login with incorrect credentials displays a message saying incorrect credentials and stays on the page
    login_response = app.test_client().post("/login", data={
        "username": "paulthottappilly",
        "password": "password1",
    }, follow_redirects=True)

    assert login_response.status_code == 200
    assert "Login to ArtWork!" in login_response.data.decode('utf-8')

def test_logout():
    # Preconditions: The user is already logged into the account and wants to log out
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = 'paulthottappilly'

        # test logout 
        response = client.post('/logout', follow_redirects=True) 

        assert response.status_code == 200
        assert "This is the Landing Page" in response.data.decode('utf-8')

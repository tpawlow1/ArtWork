from app import app, mydb
import uuid
from freezegun import freeze_time
import requests


def test_bid():
    auction_id = str(uuid.uuid4())
    client = app.test_client()

    # test 1 - bidding without repeat bidders

    # create an artist
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testartist', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create 3 non-artists
    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser1', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser2', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    addcom = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = ('testuser3', 'testemail',
               'testpassword', 'testbio', 'bunny.jpg', 0, 1000.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    # create auction made by testartist
    addcom = "INSERT INTO Auctions VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    addvals = (auction_id, 'testtitle',
               'testdesc', 'bunny.jpg', 'testartist', '2022-12-31 12:00:00', '2023-01-01 12:00:00', 1000.00, 0, None, 0.00)
    mysqlcursor.execute(addcom, addvals)
    mydb.commit()

    freeze_time("2023-01-01 11:00:00")

    with client.session_transaction() as session:
        session['user'] = 'testuser1'

    response = client.post('/bid', data={
        "bid": 100.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user'] = 'testuser2'

    response = client.post('/bid', data={
        "bid": 200.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user'] = 'testuser3'

    response = client.post('/bid', data={
        "bid": 300.00,
        "auction_id": f"{auction_id}"
    })

    assert response.status_code == 302

    # mysqlcursor.execute("SELECT * FROM Bids WHERE bidder='testuser1'")
    # results =

    mysqlcursor.execute("SELECT * FROM Users WHERE username='testuser1'")
    results = mysqlcursor.fetchone()

    assert 'testuser1', 900.00 in results

    mysqlcursor.execute(
        f"TRUNCATE TABLE Bids")
    mydb.commit()
    mysqlcursor.execute(
        f"TRUNCATE TABLE Auctions")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser1'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser2'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser3'")
    mydb.commit()

    # test 2 - bidding with repeat bidder

    # test 3 - bidding with insufficient funds

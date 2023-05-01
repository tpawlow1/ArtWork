from app import app, mydb
import uuid
from freezegun import freeze_time


def test_bid():
    bid_id = str(uuid.uuid4())
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

    mysqlcursor.execute(
        f"DELETE FROM Users WHERE username='testartist'")
    mydb.commit()
    mysqlcursor.execute(
        f"DELETE FROM Auctions WHERE auction_id = '{auction_id}'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser1'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser2'")
    mydb.commit()
    mysqlcursor.execute(f"DELETE FROM Users WHERE username='testuser3'")
    mydb.commit()

    # test 2 - bidding with repeat bidder

    # test 3 - bidding with insufficient funds

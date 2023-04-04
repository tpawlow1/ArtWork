from app import app, mydb
import uuid


def test_editpost():
    postid = str(uuid.uuid4())

    # connect to db and create post before editing
    mysqlcursor = mydb.cursor(buffered=True)
    addcom = "INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s)"
    addvals = (postid, 'testtitle', 'test_desc', 'bunny.jpg', 'sample', 0, 0)

    mysqlcursor.execute(addcom, addvals)
    mydb.commit()
    mysqlcursor.close()

    # test1 = good
    response = app.test_client().post(f'/edit/{postid}', data={
        "title": "test_title",
        "description": "test_description",
    })

    # not really a logged in user, so we need to check with database that the post was updated.
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    mysqlcursor.execute(f"SELECT * FROM Posts WHERE `id`='{postid}'")
    results = mysqlcursor.fetchall()

    assert "test_title", "test_description" in results

    # test 2 where no input is given
    response = app.test_client().post(f'/edit/{postid}', data={
        "title": "",
        "description": "",
    })

    # should still redirect
    assert response.status_code == 302

    mysqlcursor = mydb.cursor(buffered=True)
    query = f"DELETE FROM Posts WHERE `id`='{postid}'"
    mysqlcursor.execute(query)
    mydb.commit()

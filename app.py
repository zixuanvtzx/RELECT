from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    db = sqlite3.connect("recordings.db")
    query = """SELECT * FROM Recordings"""
    cursor = db.execute(query, ())
    data = cursor.fetchall()
    #print(data)
    cursor.close()
    db.close()
    return render_template('home.html', records=data)

@app.route('/search/', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template('search.html')
    else:
        # POST request
        username = request.form["userid"]
        db = sqlite3.connect("recordings.db")
        query = """SELECT Recordings.Dialect, Recordings.Phrase,
        Recordings.Voice FROM Recordings WHERE Recordings.Contributor = ?"""
        cursor = db.execute(query, (username,))
        data = cursor.fetchall()
        cursor.close()
        db.close()

        db = sqlite3.connect("recordings.db")
        query = """SELECT Comments.Comment, Comments.Sender FROM Comments
    WHERE Comments.DirectedUser = ?"""
        cursor = db.execute(query, (username,))
        thankdata = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template("profile.html", user=username, records=data,
                                       thanks=thankdata)
            
@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    else:
        # POST request
        username = request.form["usernameid"]
        dialect = request.form["dialectid"]
        phrase = request.form["phraseid"]
        file = request.form["fileid"]
        db = sqlite3.connect("recordings.db")
        query = '''INSERT INTO Recordings(Dialect, Phrase, Voice, Contributor)
VALUES(?,?,?,?) '''
        db.execute(query, (dialect, phrase, file, username))
        db.commit()
        db.close()
        return render_template("success.html")

@app.route("/comment/<user>/", methods=["GET", "POST"])
def comment(user):
    if request.method == "GET":
        return render_template('comment.html', username=user)
    else:
        # POST request
        comment = request.form["commentid"]
        sender = request.form["senderid"]
        db = sqlite3.connect("recordings.db")
        query = '''INSERT INTO Comments(DirectedUser, Comment, Sender)
VALUES(?,?,?) '''
        db.execute(query, (user, comment, sender))
        db.commit()
        db.close()
        return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=False)


from liquidnet import db


class User(db.Model):
    __tablename__ = 'library_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))


class BookRequests(db.Model):
    __tablename__ = 'book_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    email = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)

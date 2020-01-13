from liquidnet.library.models import User, Books, BookRequests
from liquidnet import db
import datetime
from liquidnet.library.serializer import RequestSchema


def check_user_exists(user):
    user_id = User.query.filter_by(email=user).first()
    return user_id.id if user_id else None


def create_user(user_email):
    new_user = User(email=user_email)
    db.session.add(new_user)
    db.session.commit()


def create_book():
    book1 = Books(title='Inferno', author='Dan Brown')
    book2 = Books(title='The Alchemist', author='Paulo Coelho')
    db.session.add(book1)
    db.session.add(book2)
    db.session.commit()


def list_all_request():
    request_schema = RequestSchema()
    all_request_objects = BookRequests.query.all()
    list_of_requests = [request_schema.dump(request_obj) for request_obj in all_request_objects]
    return list_of_requests


def create_request(data):
    user_email = data['email']
    title = data['title']

    user_id = check_user_exists(user_email)

    if not user_id:
        create_user(user_email)

    new_request = BookRequests(title=title,email=user_email,
                               timestamp=datetime.datetime.utcnow())
    db.session.add(new_request)
    db.session.commit()
    request_schema = RequestSchema()
    result = request_schema.dump(new_request)
    return result


def delete_request(request_id):
    request_result = BookRequests.query.get(request_id)
    if request_result:
        db.session.delete(request_result)
        db.session.commit()
    return True if request_result else False


def fetch_request_by_id(request_id):
    request_result = BookRequests.query.get(request_id)
    if not request_result:
        return
    request_schema = RequestSchema()
    result = request_schema.dump(request_result)
    return result

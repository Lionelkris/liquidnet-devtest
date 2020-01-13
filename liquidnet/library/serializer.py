from marshmallow import ValidationError, Schema, validates, fields
from liquidnet import ma
from .models import BookRequests, Books


class RequestValidationSchema(Schema):
    email = fields.Email(required=True)
    title = fields.String(required=True)

    @validates("title")
    def validate_title(self, value):
        titles = Books.query.with_entities(Books.title).all()
        # Reformatting list of tuples to a list.
        titles = [title[0] for title in titles]
        if value not in titles:
            raise ValidationError("The book with this title does not exist")


class RequestSchema(ma.ModelSchema):
    class Meta:
        model = BookRequests




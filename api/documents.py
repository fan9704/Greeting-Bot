from mongoengine import Document,StringField,DateField

class User(Document):
    email = StringField(required=True)
    gender = StringField(max_length=50)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    date_of_birth = DateField()
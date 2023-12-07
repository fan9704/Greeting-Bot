from api.documents import User
from datetime import datetime
from mongoengine import connect


class UserService:
    connect('greet')

    @staticmethod
    def get_birthday_user_queryset():
        user_queryset = User.objects.filter(
            date_of_birth__day=datetime.today().day,
            date_of_birth__month=datetime.today().month
        )
        return user_queryset

    @staticmethod
    def get_gender_discount(gender: str):
        discount_message = ""
        if gender == "Male":
            discount_message = '''
            We offer special discount 50% off for the following items:\n
            Cosmetic, LV Handbags
            '''
        elif gender == "Female":
            discount_message = '''
            We offer special discount 20% off for the following items:\n
            White Wine, iPhone X
            '''
        return discount_message

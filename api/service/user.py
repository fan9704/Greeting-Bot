from api.models import User
from datetime import datetime


class UserService:
    @staticmethod
    def get_birthday_user_queryset():
        user_queryset = User.objects.all()
        user_list = []
        for user in user_queryset:
            if user.date_of_birth.month == datetime.today().month and user.date_of_birth.day ==datetime.today().day:
                user_list.append(user)
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

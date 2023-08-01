import random
from faker import Faker
from random import randint

from . import models
from donation import settings


def generate_otp():
    return random.randint(100000, 999999)


def send_otp_to_phone_number(phone_number, otp):
    from twilio.rest import Client

    account_sid = settings.Account_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+14065217175',
        body=f'Your one time password for donation is {otp}.',
        to=f'+91{phone_number}'
    )

    print(message.sid)


class FakeDataGenerator:
    def __init__(self, count):
        self.count = count
        self.fake = Faker()

    @staticmethod
    def _get_first_and_last_name_from_name(name: str):
        return name.split(' ')[:2]

    @staticmethod
    def _get_username_from_name(name: str):
        return name.replace(' ', '_').lower()

    def _get_fake_indian_phone_number(self):
        return f'+91{self.fake.msisdn()[3:]}'

    def _generate_otp_for_signup(self):
        return ''.join([str(randint(0, 9)) for _ in range(6)])

    def generate(self):

        users_to_be_created = []
        for i in range(self.count):
            name = self.fake.name()
            username = self._get_username_from_name(name=name)
            password = self.fake.password()
            contact_number = self._get_fake_indian_phone_number()

            data = {
                "username": username,
                "password": password,
                "phone_number": contact_number,
            }
            if models.User.objects.filter(username=username).exists():
                continue
            users_to_be_created.append(models.User(**data))

        models.User.objects.bulk_create(objs=users_to_be_created, batch_size=100, ignore_conflicts=True)

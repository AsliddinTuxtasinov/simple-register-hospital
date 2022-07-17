from django.test import TestCase
from django.urls import reverse

from .models import DiseasedUser


class UserTestsCase(TestCase):

    def test_user_register(self):
        data_context = {
            'first_name': "asliddin",
            'last_name': "Asliddin",
            'telephone_number': "+998887878",
            'email_address': "asliddin@gmail.com",
            'describe_your_condition': "yuragi o'griyapti nimagadur",
            'time_procedure': 5,
        }

        self.client.post(path=reverse('register'), data=data_context)
        user = DiseasedUser.objects.get(telephone_number=data_context['telephone_number'])

        self.assertEqual(first=user.id, second=1)
        self.assertEqual(first=user.first_name, second=data_context['first_name'])
        self.assertEqual(first=user.last_name, second=data_context['last_name'])
        self.assertEqual(first=user.telephone_number, second=data_context['telephone_number'])
        self.assertEqual(first=user.email_address, second=data_context['email_address'])
        self.assertEqual(first=user.describe_your_condition, second=data_context['describe_your_condition'])
        self.assertEqual(first=user.time_procedure, second=data_context['time_procedure'])

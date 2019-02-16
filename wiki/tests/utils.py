from django.contrib.auth import get_user_model
from django.test import Client, TestCase


HTTP_OK = 200
HTTP_404 = 404


class AdminUserTestCase(TestCase):

    def setUp(self):
        super(AdminUserTestCase, self).setUp()
        username = 'admin@bulubox.com'
        password = 'Pank8888'
        self.user = get_user_model().objects.create_superuser(
            username=username,
            email=username,
            password='Pank8888',
        )
        self.client = Client()
        self.client.login(username=username, password=password)

from django.test import TestCase
import os
from django.contrib.auth.password_validation import validate_password


class TryDjangoConfigTest(TestCase):
    def test_secret_key_strength(self):
        # settings.SECRET_KEY
        secret_key = os.environ.get('DJANGO_SECRET_KEY')
        # self.assertNotEqual(SECRET_KEY, 'abc123')
        try:
            validate_password(secret_key)
        except Exception as e:
            msg = f"Bad Secret Key {e.messages}"
            self.fail(msg)

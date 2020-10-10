
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
"""
Genrating User Verification Token To send into the Email
"""
class emailVerifi(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active) +text_type(user.pk) +text_type(timestamp))

email_token = emailVerifi()
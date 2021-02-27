from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist



class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, request, email=None, code=None):

        try:
            user = User.objects.get(email=email)
            try:
                if user.student.login_code == code:
                    user.student.login_code = None
                    user.student.save()
                    return user
            except ObjectDoesNotExist:
                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
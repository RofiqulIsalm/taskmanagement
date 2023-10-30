from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self,username = None, password = None, **kwargs):
        UserMonel = get_user_model()
        
        try:
            user = UserMonel.objects.get(username = username)
        except UserMonel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
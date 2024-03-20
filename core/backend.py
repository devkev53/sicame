from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthEmailBackend(ModelBackend):
  def authenticate(self, request, username=None, password=None, **kwargs):
    try:
      # Toma el email del usuario
      user = User.objects.get(email=username)
      # Chequea que el password sea correcto
      if user.check_password(password):
        # Retorna el Usuario
        return user
    except ObjectDoesNotExist:
      return None

  def get_user(self, user_id):
    try:
      # Retorna el id del usuario
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
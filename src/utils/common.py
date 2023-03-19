from mipac.models import LiteUser

def get_name(user: LiteUser):
    return user.name if user.name else user.username

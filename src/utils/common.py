from mipac.models import LiteUser


def get_name(user: LiteUser):
    return user.nickname if user.nickname else user.username

from main.models.post.models import *
from main.models.user.models import *
class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        post = Post.objects.all()
        user = CustomUser.objects.all()
        return context


def verify_email():
    pass

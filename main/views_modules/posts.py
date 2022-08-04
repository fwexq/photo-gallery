from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django.urls import reverse
from main.forms import PostForm


class UpdatePostView(UpdateView):
    model = get_user_model()
    form_class = PostForm
    template_name = 'main/posts/update.html'

    # def get_object(self):
    #     return self.model.objects.get(id=self.request.user.id)

    def put(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('posts_detail', kwargs={'pk': self.object.pk})
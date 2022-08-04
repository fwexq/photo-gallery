# from django.contrib import messages
# from django.forms import TextInput, Textarea
# from service_objects.services import Service
# from main.models import Post
# from django.shortcuts import render
#
#
# class CreatePostService(Service):
#     def __init__(self, *args, **kwargs):
#         super(CreatePostService, self).__init__(*args, **kwargs)
#         self.fields['title'].label = ''
#         self.fields['description'].label = ''
#         self.fields['photo'].label = ''
#
#     class Meta:
#         model = Post
#         fields = ('title', 'description', 'photo')
#
#         widgets = {
#             "title": TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название', 'style': 'width:27%'}),
#             "description": Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание', 'style': 'height:8%'}),
#         }
#
#     def process(self):
#         post_form = CreatePostService()
#         return render(self.request, 'main/create.html', {'post_form': post_form})
#
#     def post_process(self):
#         active_user = self.request.user
#         post_form = CreatePostService(self.request.POST, self.request.FILES)
#
#
#         if post_form.is_valid():
#             instance = post_form.save(commit=False)
#             instance.custom_user_first_name = active_user
#             instance.save()
#             messages.success(
#                 self.request,
#                 "Пост был успешно добавлен!"
#             )
#         return render(self.request, 'main/create.html', {'post_form': post_form})
#

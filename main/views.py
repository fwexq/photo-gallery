import os
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from rest_framework.response import Response
from rest_framework import generics
from .forms import *
from main.utils import DataMixin
from .models.post.models import Post
from .serializers import PostSerializer
from rest_framework.authtoken.models import Token

class AuthorizationView(DataMixin, TemplateView):
    template_name = os.path.join('main/accounts', 'authorizations.html')
    redirect_authenticated_user = True
    sign_up_form_class = RegisterUserForm
    sign_in_form_class = LoginUserForm

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        sign_up_form = self.sign_up_form_class()
        sign_in_form = self.sign_in_form_class()
        context['sign_up_form'] = kwargs.get('sign_up_form', sign_up_form)
        context['sign_in_form'] = kwargs.get('sign_in_form', sign_in_form)
        return context

    def sign_up_form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse_lazy('profile'))

    def sign_in_form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(reverse_lazy('posts_list'))

    def post(self, request):
        post_data = request.POST or None
        sign_up_form = self.sign_up_form_class(data=post_data)
        sign_in_form = self.sign_in_form_class(data=post_data)
        context = self.get_context_data(sign_up_form=sign_up_form,
                                        sign_in_form=sign_in_form)
        if post_data.get('action') == 'sign_up':
            if sign_up_form.is_valid():
                return self.sign_up_form_valid(sign_up_form)
        if post_data.get('action') == 'sign_in':
            if sign_in_form.is_valid():
                return self.sign_in_form_valid(sign_in_form)
            else:
                return self.render_to_response(context)
        return self.render_to_response(context)

class TokenView(View):
    model = CustomUser
    form_class = TokenForm

    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)

        if user.api_key == '':
            user.api_key = str(Token.objects.create(user=request.user))
            user.save()
        else:
            user.api_key = ''
            Token.objects.get(user_id=request.user.id).delete()
            user.save()
            user.api_key = str(Token.objects.create(user=request.user))
            user.save()
        return render(request, 'main/accounts/profile.html')

    def get(self, request):
        form = TokenForm()
        return render(request, 'main/accounts/profile.html', {'form': form})


    def get(self, request):
        form = TokenForm()
        return render(request, 'main/accounts/profile.html', {'form': form})


class ProfileView(ListView):
    model = CustomUser
    template_name = 'main/accounts/profile.html'
    context_object_name = 'prof'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs['pk'])
        return render(request, 'main/accounts/profile.html', {'user': user})



class ProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'main/accounts/profile_update.html'

    def get_object(self):
        return self.model.objects.get(id=self.request.user.id)

    def put(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ListPostView(DataMixin, ListView):
    paginate_by = 4
    model = Post
    template_name = 'main/posts/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(moderation_status='VALID').order_by('-publicated_at')
        return posts


class DetailPostView(DataMixin, View):
    def get(self, request, *args, **kwargs):
        post_obj = Post.objects.get(pk=kwargs['det'])
        comments = post_obj.comments.all()
        user = request.user.id
        comment_form = CommentForm()
        return render(request,
                      'main/posts/detail.html',
                      {'post_obj': post_obj,
                       'user': user,
                       'comments': comments,
                       'comment_form': comment_form})

    def comments(request):
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            post_id = request.POST.get('post_id')
            post_obj = Post.objects.get(id=post_id)
            comments = Comment.objects.all()
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post_obj
                new_comment.save()
        else:
            comment_form = CommentForm()
        return render(request,
                      'main/posts/detail.html',
                      {'post_obj': post_obj,
                       'comments': comments,
                       'comment_form': comment_form})


class PostModerationListView(ListView):
    model = Post
    template_name = 'main/posts/list_for_moderators.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Объявления без модерации'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('posts_list')

    def get_queryset(self):
        posts = Post.objects.filter(moderation_status='NOT_MODERATED').order_by('-created_at')
        return posts


class PostRejectedView(ListView):
    model = Post
    template_name = 'main/posts/posts_rejected.html'
    context_object_name = 'posts'
    POST_STATUS_MAPPER = {'rejected': 'INVALID', 'published': 'VALID', 'moderated': 'NOT_MODERATED'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_type'] = self.kwargs.get('status')
        return context


    def get_queryset(self):
        moderation_status = self.POST_STATUS_MAPPER.get(self.kwargs.get('status'))
        if moderation_status:
            posts = Post.objects.filter(moderation_status=moderation_status, author=self.request.user).order_by('-created_at')
        else:
            posts = Post.objects.none()
        return posts


class PostPublishedView(ListView):
    model = Post
    template_name = 'main/posts/posts_published.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(moderation_status='VALID', author=self.request.user).order_by('-created_at')
        return posts


class PostModeratedView(ListView):
    model = Post
    template_name = 'main/posts/posts_moderated.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(moderation_status='NOT_MODERATED', author=self.request.user).order_by('-created_at')
        return posts

class PostValidView(View):
    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['det'])
        print(post)
        post.moderation_status = 'VALID'
        post.publicated_at = timezone.now()
        post.save()
        return redirect('posts_list')


class PostInvalidView(View):
    def get(self, request, **kwargs):
        posts = get_object_or_404(Post, pk=kwargs['det'])
        print(posts)
        posts.moderation_status = 'INVALID'
        posts.save()
        return redirect('posts_list')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'main/posts/update.html'
    form_class = PostForm
    context_object_name = 'post'
    pk_url_kwarg = 'det'


    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['det'])
        form = PostForm(files=request.FILES, data=request.POST, instance=post)
        print(form.is_valid())
        print(form.errors.as_data())
        if form.is_valid():
            post.moderation_status = 'NOT_MODERATED'
            post.publicated_at = timezone.now()
        post.save()
        return redirect('posts_list')


class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'det'
    template_name = 'main/posts/confirm_delete.html'

    success_url = reverse_lazy('posts_list')


class Search(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        res_search = self.request.query_params.get('search', "")
        results = Post.objects.filter((Q(title__icontains=res_search)
                                     | Q(description__icontains=res_search)))
                                     # | Q(author__icontains=res_search)))
        return Response({'posts': PostSerializer(results, many=True).data})


class LikesView(DataMixin, DetailView):
    model = Post
    template_name = 'main/posts/detail.html'
    pk_url_kwarg = 'like'
    context_object_name = 'det_post'

    def post(self, request):
        user = request.user
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        data = {
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)

        return redirect('posts_list')

class CommentsView(View):
    form_class = CommentForm
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['det'])
        post.comments.create(text=request.POST['text'], user_id=request.user.id)
        return redirect('posts_detail', det=post.id)


class CreatePostView(CreateView, View):
    form_class = CreatePostForm
    template_name = 'main/posts/create.html'

    def post(self, request, *args, **kwargs):
        post_form = CreatePostForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(
                request,
                "Пост был успешно отправлен на модерацию"
            )
            return render(request, 'main/posts/create.html', {'post_form': post_form})

    def get(self, request, *args, **kwargs):
        post_form = CreatePostForm()
        return render(request, 'main/posts/create.html', {'post_form': post_form})


def logoutuser(request):
    logout(request)
    return redirect('posts_list')


class StaffList(ListView):
    model = CustomUser
    context_object_name = 'title'
    template_name = 'main/job_title/title.html'


    def get_queryset(self):
        staff = CustomUser.objects.filter(is_superuser=True, is_staff=True).order_by(Lower('last_name'))
        return staff


class CreateStaff(View):
    model = CustomUser
    context_object_name = 'title'
    template_name = 'main/job_title/create_staff.html'
    form_class = CreateJobTitle

    def put(self, request, *args, **kwargs):
        post_form = CreateJobTitle(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts_list')


    def get(self, request):
        form = CreateJobTitle()
        return render(request, 'main/job_title/create_staff.html', {'form': form})


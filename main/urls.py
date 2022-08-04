from django.urls import path
from .views import *

urlpatterns = [

    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('token/', TokenView.as_view(), name='token'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile_update'),

    path('', ListPostView.as_view(), name='posts_list'),
    path('create/', CreatePostView.as_view(), name='posts_create'),
    path('update/<int:det>/', PostUpdateView.as_view(), name='posts_update'),
    path('delete/<int:det>/', PostDeleteView.as_view(), name='posts_delete'),
    path('detail/<int:det>/', DetailPostView.as_view(), name='posts_detail'),
    path('post/moderation/', PostModerationListView.as_view(), name='post_list_moderation'),


    # path('post/<int:det/>', UpdatePostView.as_view(), name='upd_post'),
    path('posts/<str:status>/', PostRejectedView.as_view(), name='account_posts_list'),
    # path('post/<str:status>/', PostRejectedView.as_view(), name='posts_publised'),
    # path('post/<str:status>/', PostRejectedView.as_view(), name='posts_moderated'),


    path('detail/<int:det>/comments/', CommentsView.as_view(), name='comments'),
    path('likes/', LikesView.as_view(), name='posts_like'),
    path('valid/<int:det>/', PostValidView.as_view(), name='valid'),
    path('invalid/<int:det>/', PostInvalidView.as_view(), name='invalid'),

    path('search/', Search.as_view(), name='search'),
    path('logout/', logoutuser, name='logout'),

    path('staff_list/', StaffList.as_view(), name='staff_list'),
    path('create_staff/', CreateStaff.as_view(), name='create_staff'),

]


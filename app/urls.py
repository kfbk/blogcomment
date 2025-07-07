from django.urls import path
from .views import PostListView,PostDetail, PostListByCategoryView,PostListByMonthView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    # 名前変更 PostDetailView --> PostDetail
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostListByCategoryView.as_view(), name='post_list_by_category'), #追加
    path('archive/<int:year>/<int:month>/', PostListByMonthView.as_view(), name='post_list_by_month'), #追加
    # path('create', views.PostNew, name='add_form'),  # 追記
    path('post/new/', views.CreatePostView.as_view(), name='add_form'),
    path('post/edit/<int:pk>/', views.EditPostView.as_view(), name='post_edit'), # 追加
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]
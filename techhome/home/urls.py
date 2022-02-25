from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = "home"),
    path('article/<int:pk>', views.ArticleView.as_view(), name = "article"),
    path('category', views.CategoryView.as_view(), name = "category"),
    path('authors', views.docsView.as_view(), name = "docs"),
    path('category/<int:pk>', views.catPage.as_view(), name = "category-page"),
    path('like/<int:pk>', views.LikeView, name="like_post"),
    path('like/author/<int:pk>', views.LikeAuthorView, name="like_author"),
    path('dislike/<int:pk>', views.DisLikeView, name="dislike_post"),
    path('search', views.search_posts, name="search"),
    path('new/article', views.AddPostView.as_view(), name="newpost"),
    path('review/articles', views.ReviewPostView.as_view(), name="review"),
    path('review/articles/<int:pk>', views.ReviewCatPostView.as_view(), name="review-posts"),
    path('accept/<int:pk>', views.ApproveView, name="accept"),
]

#path('about.html', views.about, name = "about"),

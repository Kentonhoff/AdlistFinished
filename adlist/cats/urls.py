from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.CatListView.as_view()),
    path('cats', views.CatListView.as_view(), name='cats'),
    path('cat/<int:pk>', views.CatDetailView.as_view(), name='cat_detail'),
    path('cat/create',
        views.CatFormView.as_view(success_url=reverse_lazy('cats')), name='cat_create'),
    path('cat/<int:pk>/update',
        views.CatFormView.as_view(success_url=reverse_lazy('cats')), name='cat_update'),
    path('cat/<int:pk>/delete',
        views.CatDeleteView.as_view(success_url=reverse_lazy('cats')), name='cat_delete'),
    path('cat_picture/<int:pk>', views.stream_file, name='cat_picture'),
    path('cat/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('cats')), name='comment_delete'),
]

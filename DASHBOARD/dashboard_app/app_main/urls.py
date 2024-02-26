from django.urls import re_path, path
from app_main import views
from app_main.views import ToDoListView, SpendingsListView,  ToDoDetailView, ToDoUpdateView, ToDoDeleteView
from app_main.views import SpendingsDetailView, SpendingsUpdateView, SpendingsDeleteView, DashboardView

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    # path('page-user/', views.pageuser, name='page-user'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('ai/', views.ai, name='ai'),

    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('to-do/', ToDoListView.as_view(), name='to-do'),
    path('to-do-add/', views.todoadd, name='to-do-add'),
    path('to-do/<int:pk>/', ToDoDetailView.as_view(), name='to-do-detail'),
    path('to-do/<int:pk>/edit/', ToDoUpdateView.as_view(), name='to-do-update'),
    path('to-do/<int:pk>/delete/', ToDoDeleteView.as_view(), name='to-do-delete'),


    path('spendings/', SpendingsListView.as_view(), name='spendings'),
    path('spendings-add/', views.spendingsadd, name='spendings-add'),
    path('spendings/<int:pk>/', SpendingsDetailView.as_view(), name='spendings-detail'),
    path('spendings/<int:pk>/edit/', SpendingsUpdateView.as_view(), name='spendings-update'),
    path('spendings/<int:pk>/delete/', SpendingsDeleteView.as_view(), name='spendings-delete'),


]
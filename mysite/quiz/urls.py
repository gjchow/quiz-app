from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('list/', views.listing, name='list'),
    path('list/<str:search>/', views.search_list, name='search'),
    path('quiz-mc/', views.quiz_mc, name='quiz-mc'),
    path('quiz-text/', views.quiz_text, name='quiz-text'),
    path('check-ans/<str:quiz>/<str:given>/', views.check_ans, name='check-ans'),
    path('add-new/', views.add_new, name='add-new'),

]

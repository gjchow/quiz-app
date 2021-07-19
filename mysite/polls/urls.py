from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('list/', views.ResultsView.as_view(), name='list'),
    path('quiz-mc/', views.quiz_mc, name='quiz-mc'),
    path('quiz-text/', views.quiz_text, name='quiz-text'),
    path('check-ans/<str:quiz>/<str:given>/', views.check_ans, name='check-ans'),
    path('add-new/', views.add_new, name='add-new'),

]

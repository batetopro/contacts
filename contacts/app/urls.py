from django.urls import path

from . import views


app_name = 'app'
urlpatterns = [
    path('', views.ListContactsView.as_view(), name='list_contacts'),
    path('<str:username>/', views.GetContactView.as_view(), name='single_contact'),
]

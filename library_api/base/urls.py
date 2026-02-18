from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    # path('add/', views.addBook, name='add'),
    path('library/add/', views.add_book, name='add-book'),
    path('update/<int:pk>/', views.updateBook, name='update'),
    path("api/books/delete/<int:pk>/", views.delete_book, name="delete_book"),

]
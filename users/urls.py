from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name='login'),
    path('singup/', views.singup,name='singup'),
    path('home/', views.home,name='home'),
    path('logout/', views.logout,name='logout'),
    path('admin/', views.adminpanel,name='adminpanel'),
    path('dashboard/', views.admindashboard,name='dashboard'),
    path('logoutadmin/', views.logoutadmin,name='logoutadmin'),
    path('delete/<int:id>', views.delete,name="delete"),
    path('update/<int:id>', views.update,name='update'),
    path('updated/<int:id>', views.updated,name='updated'),
    path('create/', views.create,name='create')
]
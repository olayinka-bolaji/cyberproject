from django.urls import path

# local modules
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('confirm/<int:tok>/', views.confirmAccount, name='confirm'),
    path('forgot-password/', views.forgotPassword, name='forgotpass'),
    path('change-password/<str:pk>', views.changePassword, name='changepass'),
    path('reset/<int:tok>', views.resetPassword, name='reset'),
    path('book-appointment/', views.bookAppointment, name='book-appointment'),
]
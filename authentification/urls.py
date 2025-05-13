from django.urls import path
from . import views
app_name = 'authentification'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin, name='admin'),
    path('liste-boutiques/', views.liste_boutiques, name='liste_boutiques'),
    path('activate-boutique/', views.activate_boutique, name='activate_boutique'),
    path('deactivate-boutique/', views.deactivate_boutique, name='deactivate_boutique'),

    # Password reset URLs
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-change/', views.password_change, name='password_change'),
]

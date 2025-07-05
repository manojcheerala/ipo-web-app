from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Public Pages
    path('', views.home, name='home'),
    path('ipo-detail/<int:pk>/', views.ipo_detail, name='ipo-detail-page'),
    path('ipo/upcoming/', views.upcoming_ipos, name='upcoming-ipos'),
    path('dashboard/ipo-table/', views.ipo_table_view, name='ipo-table'),
path('dashboard/ipo/edit/<int:pk>/', views.edit_ipo_view, name='edit-ipo'),
path('dashboard/ipo/delete/<int:pk>/', views.delete_ipo_view, name='delete-ipo'),


    # API Endpoints
    path('api/ipo/', views.ipo_api_view, name='ipo-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom Admin Auth
    path('dashboard/login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('dashboard/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/register/', views.register_view, name='register'),
    
    # Password Reset / Change
    path('dashboard/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='admin/password_reset.html'), name='password_reset'),
    path('dashboard/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='admin/password_reset_done.html'), name='password_reset_done'),
    path('dashboard/password-change/', auth_views.PasswordChangeView.as_view(
        template_name='admin/password_change.html'), name='password_change'),
    path('dashboard/password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='admin/password_change_done.html'), name='password_change_done'),
         path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
         path('dashboard/add-ipo/', views.add_ipo_view, name='add-ipo'),

]
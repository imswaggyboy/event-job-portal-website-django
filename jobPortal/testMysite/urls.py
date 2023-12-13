
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from user.views import register,profile,user_info
from jobs.views import (JobsListView,
                        JobsCreateView,
                        JobDetailView,
                        JobUpdateView,
                        JobDeleteView,
                        AppliedUserView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    path('', include('blog.urls')), 
    path('register/', register, name='register'),
    path('profile_info/', user_info, name='profile_info'),
    path('profile/<str:username>/', profile, name='profile'),
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),
        name='password_reset'),
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password_reset_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
        name='password_reset_complete'),

    path('jobs/', JobsListView.as_view(), name='jobs-list'),
    path('my-jobs/<int:user_id>/', JobsListView.as_view(), name='my-jobs-list'),
    path('jobs/new/', JobsCreateView.as_view(), name='jobs-new'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='jobs-detail'),
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='jobs-update'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='jobs-delete'),
    path('jobs/applied-user/<int:jobs_id>/', AppliedUserView.as_view(), name='applied-user'),

    path('chat/',include('chats.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
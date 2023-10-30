from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name="base"),
    
    # for user atorezation 
    path('', views.Login, name="login_page"),
    path('dologin/', views.dologin, name='dologin_page'),
    path('dologout/', views.dologout, name='dologout_page'),
    path('register/', views.register, name="register_page"),
    path('forgot/', views.forgot, name="forgot_page"),
    path('profile/', views.profile, name="profile_page"),
    path('profile/password_change',views.password_change,name='password_change'),
    
    
    path('desh/', views.desh, name='desh_page'),
    path('add_task/', views.add_task, name='add_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('search/', views.search_task, name='search_task'),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

from django.urls import path,include
# from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('Userlogin', views.Userlogin, name='Userlogin'),
    path('Userlogout', views.Userlogout, name='Userlogout'),
    path('register', views.register, name='register'),
    path('invest', views.invest, name='invest'),
    path('ideas', views.ideas, name='ideas'),
    path('profile', views.profile, name='profile'),
    path('idea_provider/<int:Idea_id>/', views.idea_provider, name='idea_provider'),
    # path('package_1', views.package_1, name='package_1'),
    # path('package_2', views.package_2, name='package_2'),
    path('invest_idea/<int:Idea_id>/', views.invest_idea, name='invest_idea'),
    path('billing/<int:Idea_id>/', views.billing, name='billing'),
    path('agent_call_request/<int:Idea_id>/', views.agent_call_request, name='agent_call_request'),
    path('deposit/', views.deposit, name='deposit'),
    path('contact', views.contact, name='contact'),
    path('example_idea', views.example_idea, name='contact'),
    path('allusers', views.allusers, name='allusers'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('details_edit', views.details_edit, name='details_edit'),

]

from django.urls import path
from .views import index, other_page, BBLogin_View, profile, BBLogout_View, ProfileEditView, PasswordEditView, RegisterView, RegisterDoneView, user_activate, ProfileDeleteView, blog, posted_detail, profile_posted_add


app_name = 'main'
urlpatterns = [
 path('accounts/profile/add/', profile_posted_add, name='profile_bb_add'),
 path('accounts/profile/<int:pk>/', posted_detail, name='profile_bb_detail'),
 path('<int:pk>/', posted_detail, name='posted_detail'),
 path('<str:page>/', other_page, name='other'),
 path('', index, name='index'),
 path('accounts/login/', BBLogin_View.as_view(), name='login'),
 path('accounts/profile/', profile, name='profile'),
 path('accounts/logout/', BBLogout_View.as_view(), name='logout'),
 path('accounts/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
 path('accounts/password/edit/', PasswordEditView.as_view(), name='password_edit'),
 path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
 path('accounts/register/', RegisterView.as_view(), name='register'),
 path('accounts/activate/<str:sign>/', user_activate, name='activate'),
 path('accounts/profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
 path('blog/', blog, name='blog'),
]
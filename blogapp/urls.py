from django.urls import path
from . import views 


urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post, name="post"),
    path('category/<slug:slug>/', views.category, name='category'),
    path('tag/<slug:slug>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    
    path("user_profile/<str:pk>/", views.profile, name="profile"),
    path("my_account/", views.my_account, name="account"),
    path("update_profile/", views.UpdateProfile, name="update_profile"),
    path("delete_account/", views.DeleteProfile, name="delete_account"),
]
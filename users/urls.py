from django.urls import path

from .views import (
    login_view, logout_view, signup, 
    check_username_availability,
    create_poll, create_question, 
    edit_question
    )

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('signup/', signup, name="signup"),
    
    
    path('create_poll', create_poll, name="create_poll"),
    
    #htmx urlpatterns
    path('check_username/', check_username_availability, name="check-username"),
    path('logout/', logout_view, name="logout"),
    
    
    path('create_question/', create_question, name="create_question"),
    path('edit_question/', edit_question, name="edit_question"),
    
]
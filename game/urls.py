# poker_app/game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                      views.home,       name='home'),
    path('signup/',               views.signup,     name='signup'),
    path('rooms/',                views.room_list,  name='room_list'),
    path('rooms/<int:room_id>/join/', views.join_room, name='join_room'),
    path('rooms/<int:room_id>/',      views.game,      name='game'),
    path('rooms/<int:room_id>/results/', views.results, name='results'),
]
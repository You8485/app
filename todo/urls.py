
from django.urls import path
from . import views
app_name='todo'
urlpatterns = [
    path('',views.user_login,name="login_url"),
    path('registration/',views.registration,name="register_url"),
    path('index/',views.index,name="homepage"),
    path('index/add_new_task/',views.add_new_task,name="newtask"),
    path('index/get_task/',views.get_task,name="gettask"),
    path('index/delete_task/',views.delete_task,name="deltask"),
    path('index/edit_task/<str:pk>/',views.edit_task,name="edittask"),
    path('logout/',views.user_logout,name="logout"),
]

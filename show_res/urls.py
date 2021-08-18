# from django.urls import path 

# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
# ]

from django.urls import path

from . import views 

urlpatterns=[
    path('', views.sh, name='sh' ),
    path('result/', views.show_enrolled_stu_result, name='show_enrolled_stu_result' )


]
from django.urls import path
from . import views

urlpatterns = [

    path('',views.home),
    path('home', views.home),
    path('log_reg',views.regpage),
    path('register', views.create_user), #PASS CREATE USER
    path('login', views.login), #PASS initial html
    path('login/registration',views.login), #PASS LOGIN
    path('success/login', views.logged_in),#PASS
    path('success/registered', views.registered), #PASS 
    path('log_out', views.log_out), #PASS ERASE r.s 
    path('message', views.create_post), #PASS CREATED A POST 
    path('blog', views.display_post), #PASS DISPLAYS A POST
    path('delete_post/<int:id>', views.delete_post), #PASS DELETE A POST
    path('add_comment/<int:id>', views.create_comment),  #PASS create and add comments
    path('delete/<int:id>', views.delete_comment), #PASS delete a COMMENT by POST ID
    path('like/<int:id>', views.gets_likes), #PASS adds likes to db
    path('library', views.subject_lib), 
    path('account', views.profile),
    path('about', views.about),
    path('Resources', views.about),
    path('create_course', views.create_course),
    path('search', views.search_result),
    path('subject', views.subject_lib),
    # path('upload.php', views.profile),
    path('profile', views.profile),
    path('profile', views.course_display),
    path('courses/<int:id>/destroy', views.delete),




]
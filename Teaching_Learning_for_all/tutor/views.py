from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib import messages
from django.db import models
from .models import *
import bcrypt
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from  tutor import handle_uploaded_file



def regpage(request):
    return render(request, "login.html")



def create_user(request): #PASS
    # pass the post data to the method we wrote and save the response in a variable called errors
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        if errors:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for e in errors:
                error(request, e)
        # redirect the user back to the form to fix the errors
            return redirect('/login/registration')
        # if the errors object is empty, that means there were no errors!

        else:  #PASS THIS HELPS HASH THE PASSWORD
            hashed_pw = bcrypt.hashpw(request.POST['psw'].encode(),bcrypt.gensalt()).decode()   # ADD DECODE METHOD TO THE END
            user = User.objects.create( 
                first_name = request.POST['first_name'], 
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hashed_pw,
                birthday = request.POST['bday']
            )
            request.session['userid']=user.id

        return redirect('/success/registered')



def login(request): #PASS 
    email = User.objects.filter(email=request.POST['email'])

    if len(email) > 0:
        logged_user = email[0]

        if bcrypt.checkpw(request.POST['psw'].encode(),logged_user.password.encode()): # COMPARES THE EXISTED PSW MATCH
            request.session['userid'] = logged_user.id
            return redirect('/success/login')
        else:
           messages.error(request,"Email and Password did not match")
    else:
        messages.error(request,"This email has not been registered yet!")
    return redirect('/login/registration')




def logged_in(request): # PASS 
    context = {
        'user': User.objects.get(id = request.session['userid'])

    }
    return render(request, "profile.html", context)




def registered(request):   #PASS 
    context = {
        'user': User.objects.get(id = request.session['userid'])
    }
    return render(request, "profile.html",context)




def home(request):
    if 'user_id' in request.session:
        context = {'logged_user' : User.objects.get(id=request.session['user_id'])}
        return render (request, 'blog.html', context)
    else:
        return render(request, "home.html")




def log_out(request):
    request.session.clear()    #pass delete the current session    
    return render(request, "home.html")




def create_post(request): #PASS creates a POST 
    the_post = WallMessage.objects.create(
        message = request.POST['message'], 
        creator = User.objects.get(id = request.session['userid'])
    )

    request.session['postid'] = the_post.id

    return redirect('/blog')




def display_post(request):  #pass displays posts
    context = {
        'wall_messages': WallMessage.objects.all().order_by("-created_at"),
        'user': User.objects.get(id = request.session['userid'])
    }
    return render(request, "blog.html", context)




def delete_post(request, id):   #PASS delete a post by creator 
    to_delete = WallMessage.objects.get(id=id)
    to_delete.delete()
    return redirect('/blog')





def create_comment(request, id): #PASS / THIS CREATES A FOREIGH KEY
    #create
    poster = User.objects.get(id=request.session['userid'])
    message = WallMessage.objects.get(id=id)
    comment = Comment.objects.create(comment=request.POST['comment'], creator=poster, wall_message=message)

    request.session['comment_id'] = comment.id

    return redirect('/blog')




def delete_comment(request, id):
    to_delete = Comment.objects.get(id=id)
    to_delete.delete()
    return redirect('/blog')


# def upload(request):
#      if request.method == "POST":
#         #  updating user image
    

def gets_likes(request, id):
    liked_message = WallMessage.objects.get(id=id)
    user_liked = User.objects.get(id=request.session['userid'])
    liked_message.user_likes.add(user_liked)
    return redirect('/blog')




def subject_lib(request):

    if 'user_id' in request.session:
        context = {
            'logged_user' : User.objects.get(id=request.session['user_id'])
        }
        return render (request, 'blog.html', context)

    else:
        return render(request, "subject_lib.html")




def profile(request):
    context = {
        'wall_messages': WallMessage.objects.all().order_by("-created_at"),
        'user': User.objects.get(id = request.session['userid']),
        "all_classes" : Class.objects.all().order_by("-created_at"), #creates access to all classes
    }
    return render (request, "profile.html", context )




def about(request): 
    return render (request, "about.html")




from .models import Class
def create_course(request):   #PASS CREATES A CLASS 

    tutor = User.objects.get(id=request.session['userid'])
    errors = Class.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for e in errors:
            error(request, e)

        return redirect('/profile')

    else:
        
        a_class = Class.objects.create(
            name = request.POST['name'],
            desc = request.POST['desc'],
            tutor = tutor

        )
        request.session['class.id'] = a_class.id
            
        return redirect("/profile")



def course_display(request, id): # PASS
    course = Class.objects.get(id = request.session['userid'])

    Context = {
        'a_class' : Class.objects.get(id = request.session['userid']),
        # 'all_classes': Class.objects.all()
    }

    return render(request,"profile.html", Context)


def search_result(request):
    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        search_result = Class.objects.all().filter(feeder__icontains=search_term)

        # context{
        #     "all_classes" : Class.objects.all()
        # }
    

    return render(request, 'subject_lib.html') 



def delete(request, id):   #PASS
    delete_a_class = Class.objects.get(id = id)
    delete_a_class.delete()

    return redirect("/profile") 

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from  import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})



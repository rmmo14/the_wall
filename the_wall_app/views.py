from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        user = User.objects.get(id = request.session['user_id'])
        if user:
            return redirect('/')
    return render(request, "index.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.my_validator(request.POST)
    c = User.objects.last()
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        c.delete()
        return redirect ('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print('hash', User.objects.all())
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
        )
        request.session['user_id'] = new_user.id
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.filter(email = request.POST['email'])
    print('email', user)
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['login_pw'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')
        else:
            messages.error(request, "Incorrect email or password")
        return redirect('/')
    messages.error(request, "No account with that information...please register")
    return redirect('/')    

def success(request):
    if 'user_id' not in request.session:
        print("not in session")
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    if user:
        context = {
            'user': user,
            'messages': Message.objects.all(),
        }
        request.session['email'] = user.email
        print('message is', Message.objects.all())
        return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def post_message(request):
    if request.method == "POST":
        if 'user_id' in request.session:
            print(request.session)
            user = User.objects.get(id=request.session['user_id'])
            Message.objects.create(message=request.POST['messages'], poster=user)
            print('messages are', Message.objects.all())
    return redirect('/success')

def post_comment(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            print(request.session)
            user = User.objects.get(id=request.session['user_id'])
            message = Message.objects.get(id=id)
            Comment.objects.create(comment=request.POST['post_comments'], poster=user, message=message)
            print('messages are', Message.objects.all())
    return redirect('/success')
from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import  Response
from django.views.decorators.csrf import csrf_protect



from .serializers import *

# Create your views here.
def user_login(request):
    context={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('todo:homepage')
        else:
            return render(request,'todo/login.html',{'error':'Enter Coreect Username or Password'})
    else:
        return render(request,'todo/login.html')

def registration(request):
    if request.method=='POST':
        form=userform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            if(password != confirm_password):
                str="Paaword not same"
                return render(request, 'todo/registration.html',{'form': form,'unique':str})
            else:
                str="Enter Unique Email ID"
                try:
                    user=User.objects.get(email=email)
                    return render(request, 'todo/registration.html',{'form': form,'unique':str})
                except User.DoesNotExist:
                    User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                    return redirect('todo:login_url')
        else:
            str="User already exists change user name and try again"
            return render(request, 'todo/registration.html',{'form': form,'unique':str})
    else:
        form=userform()
        return render(request, 'todo/registration.html',{'form': form})


def index(request):
    print(request.user)
    obj=Task.objects.filter(username_id=request.user)
    print(obj)

    return render(request,'todo/task.html')


@api_view(['POST'])
def add_new_task(request):
    print('\n\n\n', request.data, '\n\n\n')
    task=request.data['task']
    if(len(task)==0):
        print('Not to do anything')
    else:
        username_id=request.user
        title=task
        obj=Task(username_id=username_id,title=task)
        obj.save()
    return Response('What!')

@api_view(['GET'])
def get_task(request):
    tasks=Task.objects.filter(username_id=request.user)
    serializers = TaskSerializers(tasks,many=True)
    return Response(serializers.data)

@api_view(['POST'])
def delete_task(request):
    task=Task.objects.get(pk=request.data['id'])
    task.delete()
    return Response('Deleted')



def edit_task(request,pk):
    print(pk)
    task=Task.objects.get(id=pk)
    form=TaskForm(instance=task)
    if request.method=="POST":
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo:homepage')
    context={
        'form': form,
    }
    return render(request,'todo/edit.html',context)

def user_logout(request):
    logout(request)
    return redirect('todo:login_url')

from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.

def singup(request):
    if request.user.is_authenticated:
        return redirect(home)

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        dic={"firstname":firstname, "lastname":lastname, "email":email, "username":username}

        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return render(request, 'singup.html',dic)

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is Taken')
                return render(request, 'singup.html',dic)
            else:
                user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                user.save()
                messages.info(request,'User Created') 
                return redirect('login')
        else:
            messages.info(request,'Password Not Matching')    
            return render(request,'singup.html',dic)
    else:
        return render(request, 'singup.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user:
            auth.login(request,user)
            return redirect(home)

        else:
            messages.info(request, 'invalid credentials') 
            return redirect('/')     
    return render(request, 'login.html')


def home(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        return render(request, 'home.html',{'user':user})
    else:
        return redirect(login)
    

def logout(request):
    auth.logout(request)
    return redirect('/')


def adminpanel(request):
    if request.session.has_key('username'):
        return redirect(admindashboard)
        
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        print(user)
        print(password)

        if user=='1234' and password=='1234':
            request.session['username'] = user
            return redirect(admindashboard) 

        else:
            messages.info(request,'invalid credentials')
            return redirect(adminpanel)

    else:
        return render(request, 'adminpanel.html')



def admindashboard(request):
    if request.session.has_key('username'):
        users = User.objects.all()
        return render(request, 'admindashboard.html',{'users':users})
    else:
        return redirect(adminpanel)

def logoutadmin(request):
    request.session.flush()
    return redirect(adminpanel)     


def delete(request,id):
    if request.session.has_key('username'):
        u=User.objects.get(id=id)
        u.delete()
        return redirect(admindashboard)
    else:
        return redirect(adminpanel)


def update(request, id):
    if request.session.has_key('username'):
        con = User.objects.get(id=id)
        return render(request, 'update.html',{"con":con})
    else:
        return redirect(adminpanel)

def updated(request,id):
    if request.session.has_key('username'):
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']

            z = User.objects.get(id=id)

            z.first_name = firstname
            z.last_name = lastname
            z.username = username
            z.email = email
            z.save()
            return redirect(admindashboard)    
        else:
            return render(request,'update.html')    
    else:
        return redirect(adminpanel)

def create(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            dic={"firstname":firstname, "lastname":lastname, "email":email, "username":username}

            if password==password2:

                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username Taken')
                    return render(request, 'create.html',dic)


                elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email Taken')
                    return render(request, 'create.html',dic)

                else:
                    user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                    user.save()
                    messages.info(request,'User Created') 
                    return redirect(admindashboard)
            else:
                messages.info(request,'Password Not Matching')    
                return render(request,'create.html',dic)

        else:               
            return render(request,'create.html')
    else:
        return redirect(adminpanel)

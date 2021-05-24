from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from app.models import Product
from django.http import HttpResponse
from xcart import settings



# Create your views here.
def index(request):
    product=Product.objects.all()
    context={'product':product}
    print(request.user)
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')

def product(request):
    product=Product.objects.all()
    print(product)
    context={'product':product}
    return render(request,'product.html',context)

def testimonial(request):
    return render(request,'testimonial.html')

def why(request):
    if request.method=="POST":
        sub = request.POST['topic']
        msg = request.POST['message']
        user = request.session['username']
        info = User.objects.get(username=user)
        print(info)
        res = send_mail(
            subject = f'Hello {user}',
            message = f'''Thanks for giving your suggestion.\n We will do our best to provide you better user experience.''',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [info.email],
            fail_silently=True,
        )
        if res==1:
            messages.success(request,"Your suggestion send successfully.")
            suggestion = Suggestion(user=info,subject=sub,message=msg)
            suggestion.save()
        else:
            messages.error(request,"Some error occured")
            return render(request,'why.html')
    return render(request,'why.html')

def handleSignup(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        # user=User.objects.get(username=uname)
        # print(user)
        if User.objects.filter(username=uname).exists():
            messages.warning(request," Choose a diffirent username.")
            return redirect('/')
        if User.objects.filter(email=email).exists():
            messages.warning(request," Account already exixst with this Email Id")
            return redirect('/')
        if password!=password1:
            messages.error(request,"Pasword didn't match. Retry!")
            return redirect('/')
        
        myuser = User.objects.create_user(uname,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,'Account successfully created.')
        res = send_mail(
            subject = f'Account created successfully , {fname}',
            message = f'''Thanks for using our site.\n\nYour Information. \n\nUsername : {uname} \nName : {fname} {lname} \nEmail : {email}\nPassword : {password}''',
            from_email = 'Brightservicecentre1@gmail.com',
            recipient_list = [email],
            fail_silently=True,
        )  
        return redirect('/')

# Username se 
def handlelogin(request):
    if request.method == "POST":
        username = request.POST["uname"]
        request.session['username']=username
        print(request.session['username'])
        password = request.POST["password"]
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'User successfully logged in.')
            client_ip = request.META['REMOTE_ADDR']
            res = send_mail(
            subject = f'Login Successful',
            message = f'''{username} logged in successfully \nYour Ip is {client_ip}''',
            from_email = 'Brightservicecentre1@gmail.com',
            recipient_list = [user.email],
            fail_silently=True,
            )  
            return redirect('/')
        else:
            messages.error(request,'Retry! , something went wrong. ')
            return redirect('/')
    return redirect('/')

def handlelogout(request):
    a=request.user.email
    uname=request.user
    logout(request)
    messages.success(request, "Successfully logged out")
    res = send_mail(
            subject = f'Successfully logout',
            message = f'''{uname} logged out successfully.''',
            from_email = 'Brightservicecentre1@gmail.com',
            recipient_list = [a],
            fail_silently=True,
            )  
    return redirect("/")

def cart(request,prod_id):
    if request.user.is_authenticated:
        try:
            prod = Product.objects.get(pk=prod_id)
        except ObjectDoesNotExist:
            pass
        # else :
        #     try:
        #         cart = Cart.objects.get(user = request.user, active = True)
        #     except ObjectDoesNotExist:
        #         cart = Cart.objects.create(user = request.user)
        #         cart.save()
        #         cart.add_to_cart(prod_id)
        #         return redirect('/prodct')
        #     else:
        return redirect('/product')
    else:
        return redirect('/product')

def viewProduct(request,uid):
    prod = Product.objects.get(sno=uid)
    context= {"product":prod}
    request.session['productSelected'] = uid
    return render(request,"productDetail.html",context)


def search(request):
    if request.method=="POST":
        name = request.POST['product']
        prod = Product.objects.all().filter(name__icontains=name)
        context={"product":prod}
        return render(request,'product.html',context)
    return HttpResponse("Not Working")


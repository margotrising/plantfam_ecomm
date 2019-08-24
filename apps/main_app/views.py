from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.main_app.models import *
import bcrypt
import re
from django.core.files.storage import FileSystemStorage

from .forms import ProductForm
from .models import Product

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$')

def index(request):
    if 'user_id' in request.session: 
        context = {
            "current_user": User.objects.get(id=request.session['user_id'])
        }
    else:
        context = {}
    return render(request, 'main_app/index.html', context)

def login(request):
    if 'user_id' in request.session: 
        context = {
            "current_user": User.objects.get(id=request.session['user_id'])
        }
    else:
        context = {}
    return render(request, 'main_app/login.html', context)

def login_process(request):
    is_valid = True
    matching_user = User.objects.filter(email=request.POST['login-email'])
    if len(matching_user) < 1:
        is_valid=False
        messages.error(request,"Invalid credentials", extra_tags="error-login")

    if len(matching_user) > 0:
        print(matching_user)
        user = matching_user[0]
        pw_hash = bcrypt.hashpw(request.POST['login-pass'].encode(), bcrypt.gensalt())  

        if bcrypt.checkpw(request.POST['login-pass'].encode(), user.password.encode()):
            request.session['user_id']=user.id
            return  redirect('/')
        else: 
            is_valid = False
            messages.error(request,"Invalid credentials", extra_tags="error-login")
            print("****passwords DO NOT match")
            return redirect('/login')
    if not is_valid:
        messages.error(request,"Invalid credentials", extra_tags="error-login")
        print('****Invalid credentials')
        return redirect('/login')
    return  redirect('/')    

def register_process(request):
    is_valid = True
    if len(request.POST['reg-fname'])< 2 or not request.POST['reg-fname'].isalpha():
        is_valid=False
        messages.error(request,"First name must contain at least 2 letters", extra_tags="register")
    if len(request.POST['reg-lname'])<2 or not request.POST['reg-lname'].isalpha():
        is_valid=False
        messages.error(request,"Last name must contain at least 2 letters", extra_tags="register")
    if not EMAIL_REGEX.match(request.POST['reg-email']):
        is_valid=False
        messages.error(request,"Invalid email address", extra_tags="register")
    if EMAIL_REGEX.match(request.POST['reg-email']):
        duplicate_email = User.objects.filter(email=request.POST['reg-email'])
        if len(duplicate_email)>0:
            is_valid=False
            messages.error(request,"Email taken", extra_tags="register")
            print('Email taken')
    if not PASS_REGEX.match(request.POST['reg-pass']):
        is_valid=False
        messages.error(request,"Password must contain 1 number, 1 capital letter, and be between 8-15 characters", extra_tags="register")
    if request.POST['reg-pass'] != request.POST['reg-cpass']:
        messages.error(request,"Confirm Password did not match. Passwords must match", extra_tags="register")
        is_valid=False
        # flash("Passwords must match", "error-cpass")
    if not is_valid:
        print('there was an error registering')
        return redirect('/login')
    else:
        pw_hash = bcrypt.hashpw(request.POST['reg-pass'].encode(), bcrypt.gensalt())        
        user = User.objects.create(first_name=request.POST['reg-fname'], last_name=request.POST['reg-lname'], email=request.POST['reg-email'], password=pw_hash)
        request.session['user_id'] = user.id       
        return redirect('/register_confirm')

def register_confirm(request):
    return render(request, 'main_app/register_confirm.html')

def products(request):
    if 'user_id' in request.session: 
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "products": Product.objects.all()
        }
    else:
        context = {
            "products": Product.objects.all()
        }
    return render(request, 'main_app/products.html', context)

def view_product(request, prod_id):
    p = Product.objects.get(id=prod_id)
    if 'user_id' in request.session: 
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            "p":p
        }
    else:
        context = {
            "p":p
        }
    return render(request, 'main_app/view_product.html', context)

def add_cart(request, prod_id):
    if not 'price' in request.session:
        request.session['price'] = 0
    if not 'qty' in request.session:
        request.session['qty'] = 0
    if not 'cart' in request.session:
        request.session['cart'] = []
    
    prod=Product.objects.get(id=prod_id)
    request.session['cart'].append(prod)
    return redirect('/cart')

def cart(request):
    if 'user_id' in request.session: 
        p=request.session.get('cart')
        context = {
            "current_user": User.objects.get(id=request.session['user_id']),
            'p': p
        }
    else:
        context = {}
    return render(request, 'main_app/cart.html', context)

def view_account(request, user_id):
    if 'user_id' in request.session:
        context={
            "current_user": User.objects.get(id=user_id)
        }
        print(request.session)
    else:
        context={}
        redirect('/')
    return render(request, 'main_app/view_account.html', context)

#admin

def inventory(request):
    if request.session['user_id'] == 1:

        print(request.FILES)
        if request.method == 'POST':
            if not request.FILES:
                messages.error(request,"Please include a photo", extra_tags="error-photo")
                print("****Error photo upload")
                return redirect('/admin/inventory')
            else: 
                form = ProductForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('/admin/inventory')
        else:
            products = Product.objects.all()
            form = ProductForm
            context = {
                'products': products,
                'form': form
            }
            print("**********All products here")
            return render(request, 'main_app/product_list.html', context)
    else:
        return redirect('/')

def edit_product(request, prod_id):
    f = get_object_or_404(Product, id=prod_id)
    print('*******', f.id)

    form = ProductForm(instance=f)

    context ={
        'f': f,
        'form': form
    }
    return render(request, 'main_app/edit_product.html', context)

def edit_product_process(request, prod_id):
    if request.method == 'POST':
        prod = Product.objects.get(id=prod_id)
        print('********Edit_product_process: ', prod.photo)

        if (request.FILES):
            form = ProductForm(request.POST, request.FILES, instance=prod)
        else:
            form = ProductForm(request.POST, instance=prod)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.photo = prod.photo
            prod.save()
            return redirect('/admin/inventory')
    return redirect('/admin/inventory')

def delete_product(request, prod_id):
    if request.method == 'POST':
        product = Product.objects.get(id=prod_id)
        product.delete()
        print("*****Product deleted")
    return redirect('/admin/inventory')

def destroy(request):
    request.session.clear()
    print('***session cleared******')
    return redirect('/')
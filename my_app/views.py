from django.shortcuts import render, redirect
from . import models
import bcrypt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import Product
from django.contrib import messages
import json

def index(request):
    context={
        "categories":models.get_category()
    }
    return render(request,'index.html',context)

def display_aboutus_page(request):
    return render(request, 'aboutus.html')

def display_productlist(request,id):
    context={
        "products":models.display_category(id)
    }
    return render(request, 'products.html', context)

def display_product(request,id):
    context={
        "review":models.Review.objects.all(),
        "product":models.get_product(id)
    }
    return render(request, 'info.html', context)

def recommend_product(request):
    return render(request, 'recommend.html')

def add_review(request):
    if 'userid' in request.session:
        review=models.add_new_review(request)
        
        product=review.product
        return redirect(f'/products/{product.id}')
    else:
        return redirect('/register_form')
    
def delete(request):
    product_id = models.delete_review(request)
    return redirect('/products/{}'.format(product_id))
    
def edit(request):
    return render(request,'editreview.html')

def edit_review(request):
    updated_review = models.update_review(request)
    return redirect('/products/{}'.format(updated_review.product.id))
    
    
def display_register_form(request):
    return render(request, 'registration_form.html')

def registeration(request):
    if request.method == 'POST':
        request.session['name']=request.POST['f_name']
        errors=models.User.objects.user_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/register_form')
        else:
            models.new_user(request)
            return redirect('/')

def login(request):
    if request.method == 'POST':
        user = models.User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['name']=logged_user.first_name
                return redirect('/')
        else:
            errors=models.User.objects.login_validator(request.POST)
            if len(errors)>0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect ('/register_form')
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')

def search_item(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        products=models.Product.objects.filter(product_name__istartswith=search_str) | models.Product.objects.filter(brand__istartswith=search_str)

        data = products.values()
        return JsonResponse(list(data), safe=False)
    
def submit_recommendation(request):
    if request.method == 'POST':
        if 'userid' in request.session:
            product_name = request.POST.get('product_name')
            brand = request.POST.get('brand')
            models.PendingRecommendation.objects.create(product_name=product_name, brand=brand)
            return HttpResponseRedirect('/thank-you')  # Redirect to a thank you page after submission
    return redirect('/register_form')
    
def get_thanks_to_user(request):
    return render(request, 'thankyou.html')
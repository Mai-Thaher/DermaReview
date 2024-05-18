from django.db import models
from django.shortcuts import render, redirect
import re
import bcrypt
from django.shortcuts import get_object_or_404
# Create your models here.
class UserManager(models.Manager):
    def user_validator(self,postdata):
        errors={}
        if len(postdata['f_name'])<2:
            errors['f_name']="First name should be at least 2 characters"
        if postdata['f_name'].isalpha() == False:
            errors['f_name']="First name should contain letters only"
        if len(postdata['l_name'])<2:
            errors['l_name']="Last name should be at least 2 characters"
        if postdata['l_name'].isalpha() == False:
            errors['l_name']="Last name should contain letters only"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postdata['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postdata['password'])<8:
            errors['password']="Password should be at least 8 characters"
        if postdata['password']!= postdata['c-password']:
            errors['password']="The password field does not match the confirm password field"
        if len(User.objects.filter(email=postdata["email"])) > 0:
            errors["duplicated_email_error"] = "Email is already existed"
        return errors
        
    
    def login_validator(self,postdata):
        errors={}
        if len(User.objects.filter(email=postdata["email"])) == 0:
            errors['user']="The entered email is not exist, if you don't have an account please fill the registration form."
        return errors
    
class PendingRecommendation(models.Model):
    product_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=255, unique=True)
    password=models.CharField(max_length=255)
    confirm_password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=UserManager()

class Product(models.Model):
    product_name=models.CharField(max_length=45)
    product_description=models.TextField()
    brand=models.CharField(max_length=45)
    img_url=models.TextField()
    user=models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    category_name=models.CharField(max_length=45)
    category_description=models.TextField(default='some description')
    category_img=models.CharField(max_length=255, default='static/img/eye-cream.jpg')
    products=models.ManyToManyField(Product,related_name="categories")
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    review_content=models.TextField()
    user=models.ForeignKey(User, related_name="reviews", on_delete = models.CASCADE)
    product=models.ForeignKey(Product, related_name="reviews", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment_content=models.TextField()
    user=models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    review=models.ForeignKey(Review, related_name="comments", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

def new_user(request):
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    c_password = request.POST['c-password']
    confirm_pw_hash = bcrypt.hashpw(c_password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create(first_name=request.POST['f_name'], last_name=request.POST['l_name'],email=request.POST['email'], password=pw_hash, confirm_password=confirm_pw_hash)

def get_product(id):
    return Product.objects.get(id=id)

def get_category():
    return Category.objects.all()

def get_review(id):
    return Review.objects.get(id=id)

def display_category(id):
    category=Category.objects.get(id=id)
    return category.products.all()

def add_new_review(request):
    review=Review()
    
    product=Product.objects.get(id=request.POST['product_id'])
    user=User.objects.get(id=request.session['userid'])
    
    review.review_content=request.POST['review']
    review.user=user
    review.product=product
    review.save()
    return review
    #return Review.objects.create(review_content=request.POST['review'], user=user, product=product)

def delete_review(request):
    review=Review.objects.get(id=request.POST['review_id'])
    product_id = review.product.id
    review.delete()
    return product_id
    

def update_review(request):
    
    review=Review.objects.get(id=request.POST['review_id'])
    review.review_content=request.POST['review_content']
    review.save()
    return review
    


    
    


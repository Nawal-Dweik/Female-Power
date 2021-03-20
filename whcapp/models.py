from django.db import models
from datetime import date, datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}')

class UserManager(models.Manager):
    def basic_validator_register(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if not postData['first_name'].isalpha():
            errors["first_name"] = "First Name should be characters only"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if not postData['last_name'].isalpha():
            errors["last_name"] = "Last Name should be characters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        if len(user):
            errors['email'] = "Email Already Exist"
        if not PW_REGEX.match(postData["password"]):
            errors["password"] = " Password should be at least 8 characters, contains small letters, capital letters, and numbers"
        if postData['confirm'] != postData['password']:
            errors["confirm"] = " Password Confirm doesn't match with password"
        return errors


    def basic_validator_login(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "wrong email address!"
        if not len(user):
            errors['email'] = "Wrong email address Or not registered"
        if len(postData['password']) < 8:
            errors["password"] = "you should enter the password"
        if len(user) and not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors["password"] = "Wrong Password!"
        return errors


class PostManager(models.Manager):
    def posts_basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters"
        if len(postData['content']) < 10:
            errors["content"] = "Content should be at least 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.TextField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.first_name + " " + self.last_name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    skills = models.TextField()
    education = models.TextField()
    education_from = models.CharField(max_length=45)
    education_to = models.CharField(max_length=45)
    experience = models.TextField()
    experience_from = models.CharField(max_length=45)
    experience_to = models.CharField(max_length=45)
    links = models.TextField()
    video_url = models.TextField()
    mobile = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Profile of " + self.user.first_name + " " + self.user.last_name

class Post(models.Model):
    title=models.CharField(max_length=45)
    content=models.TextField()
    user_post=models.ForeignKey(User,related_name="posts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    content=models.TextField()
    user = models.ForeignKey(User,related_name ='u_comments',on_delete = models.CASCADE)
    post = models.ForeignKey(Post,related_name ='m_comments',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

#form the view
def register(reg_info):
    first_name = reg_info['first_name']
    last_name = reg_info['last_name']
    email = reg_info['email']
    password = reg_info['password']
    confirm_password = reg_info['confirm']
    user = User.objects.filter(email = email)
    if len(user) == 0:
        if password == confirm_password :
            crypt_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name=first_name,last_name=last_name,email=email,password=crypt_password)
            user_info = User.objects.last()
            return user_info
    return False

def login(log_info):
    user_in_data = User.objects.filter(email=log_info['email'])
    if len(user_in_data):
        if bcrypt.checkpw(log_info['password'].encode(), user_in_data[0].password.encode()):
            return user_in_data[0]
    return False

def all_posts():
    posts = Post.objects.all()
    return posts

def logged_user(id):
    user=User.objects.get(id=id)
    return user

def addpost(post_info,user_id):
    title = post_info['title']
    content = post_info['content']
    user = User.objects.get(id=user_id)
    Post.objects.create(title=title,content=content,user_post=user)
    post = Post.objects.last()
    return post

def addcomment(comment_info,user_id):
    user=User.objects.get(id=user_id)
    post=Post.objects.get(id=comment_info['post_id'])
    comment = comment_info['comment']
    Comment.objects.create(content=comment,user=user,post=post)
    comment=Post.objects.last()
    return comment

def get_post(id):
    post= Post.objects.get(id=id)
    return post

def reg_errors(check_info):
    errors = User.objects.basic_validator_register(check_info)
    return errors

def login_errors(check_info):
    errors = User.objects.basic_validator_login(check_info)
    return errors

def posts_errors(check_info):
    errors = Post.objects.posts_basic_validator(check_info)
    return errors


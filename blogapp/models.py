from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image
import uuid

  
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
SECTION = (
        ('Popular', 'Popular'),
        ('Recent', 'Recent'),
        ('Trending', 'Trending'),
        ('Latest Post', 'Latest Post'),
    )

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to="images/")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    section = models.CharField(choices=SECTION, max_length=100)
    main_post = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateField(default=date.today)

    # Define relations
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    author  = models.ForeignKey("Profile", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    message =  models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    email = models.EmailField()
    username = models.CharField(max_length=50, null= True)
    image = models.ImageField(upload_to='media/profile_pics', blank=True)
    bio = models.TextField()
    first_name = models.CharField(max_length=50, null= True)
    last_name = models.CharField(max_length=50, null= True)
    website_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_url = models.CharField(max_length=200, null=True, blank=True)
    linkedin_url = models.CharField(max_length=200, null=True, blank=True)
    upwork_url = models.CharField(max_length=200, null=True, blank=True)
    telegram_url = models.CharField(max_length=200, null=True, blank=True)
    youtube_url = models.CharField(max_length=200, null=True, blank=True)
    github_url = models.CharField(max_length=200, null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)


    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed
    